from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from food_suggestion.models import Item
from food_suggestion.serializers import ItemSerializer, HalfCourseCombSerializer

from operator import itemgetter


@api_view(['GET', 'POST'])
def get_all_items(request):
    if request.method == 'GET':
        s = Item.objects.all()
        serializer = ItemSerializer(s, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_hotels(request):
    if request.method == 'GET':
        return Response(get_all_hotels_list())
    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_all_hotels_list():
    hotels = set()
    for item in Item.objects.all():
        hotels.add(item.hotel_name)
    return hotels


@api_view(['GET', 'PATCH'])
def get_item(request, item_id):
    if request.method == 'GET':
        item = Item.objects.get(pk=item_id)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        item = Item.objects.get(pk=item_id)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_suggestions(request, money, people, option):
    money = int(money)
    people = int(people)
    option = int(option)

    # category
    # BREAKFAST = 0
    # STARTER = 1
    # MEAL = 2
    # DESSERT = 4

    if option == 0:
        # breakfast
        # enthelum return cheyth ozhivakkanam.
        pass

    # meal, starter, dessert
    split_table = {
        1: [0, 0, 100],
        2: [0, 100, 0],
        3: [60, 40, 0],
        4: [100, 0, 0],
        5: [0, 50, 50],
        6: [75, 0, 25],
        7: [50, 30, 20]
    }

    split = split_table[option]
    meal_money = money * split[0]
    starter_money = money * split[1]
    dessert_money = money * split[2]

    # items = Item.objects.filter(hotel_name=hotel_name, price__lte=(money/people))
    items = Item.objects.filter(price__lte=(money / people))

    hotels = list(get_all_hotels_list())

    meals = {}
    starters = {}
    desserts = {}

    for hotel in hotels:
        full_courses = items.filter(category='full course', hotel_name=hotel,
                                    price__lte=(meal_money / people)).order_by('-rating')
        full_courses_serializer = ItemSerializer(full_courses, many=True)
        half_course_curry_combs = get_half_course_curry_combs(items, (meal_money / people), hotel)
        half_course_curry_combs_serializer = HalfCourseCombSerializer(half_course_curry_combs, many=True)
        h_meals = half_course_curry_combs_serializer.data
        h_meals.extend(full_courses_serializer.data)
        meals[hotel] = h_meals

        h_starters = items.filter(category='starter', hotel_name=hotel, price__lte=(starter_money / people)).order_by(
            '-rating')
        h_starters_serializer = ItemSerializer(h_starters, many=True)
        starters[hotel] = h_starters_serializer.data

        h_desserts = items.filter(category='dessert', hotel_name=hotel, price__lte=(dessert_money / people)).order_by(
            '-rating')
        h_desserts_serializer = ItemSerializer(h_desserts, many=True)
        desserts[hotel] = h_desserts_serializer.data

    suggestions = []

    for hotel in hotels:
        try:
            starter = starters[hotel][0]
            meal = meals[hotel][0]
            dessert = desserts[hotel][0]
            suggestions.append([hotel, starter, meal, dessert, starter['rating'] + meal['rating'] + dessert['rating']])
            starter = starters[hotel][0]
            meal = meals[hotel][0]
            dessert = desserts[hotel][1]
            suggestions.append([hotel, starter, meal, dessert, starter['rating'] + meal['rating'] + dessert['rating']])
            starter = starters[hotel][0]
            meal = meals[hotel][1]
            dessert = desserts[hotel][0]
            suggestions.append([hotel, starter, meal, dessert, starter['rating'] + meal['rating'] + dessert['rating']])
            starter = starters[hotel][1]
            meal = meals[hotel][0]
            dessert = desserts[hotel][0]
            suggestions.append([hotel, starter, meal, dessert, starter['rating'] + meal['rating'] + dessert['rating']])
        except IndexError:
            continue

    suggestions = sorted(suggestions, key=itemgetter(4), reverse=True)

    return Response(suggestions[:10])


def get_half_course_curry_combs(items, money, hotel):
    half_courses = items.filter(category='half course', hotel_name=hotel).order_by('-rating')
    curries = items.filter(category='curry', hotel_name=hotel).order_by('-rating')
    combs = []
    for half_course in half_courses:
        rem_money = money - half_course.price
        possible_curries = curries.filter(price__lte=rem_money)
        for pos_cur in possible_curries:
            combs.append({'half_course': half_course, 'curry': pos_cur})
    meals = []
    for comb in combs:
        meals.append({'name': comb['half_course'].name + ' and ' + comb['curry'].name,
                      'price': comb['half_course'].price + comb['curry'].price,
                      'rating': (comb['half_course'].rating + comb['curry'].rating)/2,
                      'veg': (comb['half_course'].veg & comb['curry'].veg),
                      })
    return meals


def get_half_course_curry_combs_temp(items, money, hotel):
    half_courses = items.filter(category='half course', hotel_name=hotel).order_by('-rating')
    curries = items.filter(category='curry', hotel_name=hotel).order_by('-rating')
    combs = []
    for half_course in half_courses:
        rem_money = money - half_course.price
        possible_curries = curries.filter(price__lte=rem_money)
        for pos_cur in possible_curries:
            combs.append({'half_course': half_course, 'curry': pos_cur})
    return combs
