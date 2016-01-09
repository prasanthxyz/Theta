from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from food_suggestion.models import Item
from food_suggestion.serializers import ItemSerializer, HalfCourseCombSerializer


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
def get_suggestions(request, hotel_name, money, people, option):
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

    items = Item.objects.filter(hotel_name=hotel_name, price__lte=(money/people))

    full_courses = items.filter(category='full course', price__lte=(meal_money/people)).order_by('rating')
    full_courses_serializer = ItemSerializer(full_courses, many=True)
    half_course_curry_combs = get_half_course_curry_combs(items, (meal_money/people))
    half_course_curry_combs_serializer = HalfCourseCombSerializer(half_course_curry_combs, many=True)
    meals = half_course_curry_combs_serializer.data
    meals.extend(full_courses_serializer.data)

    starters = items.filter(category='starter', price__lte=(starter_money/people)).order_by('rating')
    starters_serializer = ItemSerializer(starters, many=True)

    desserts = items.filter(category='dessert', price__lte=(dessert_money/people)).order_by('rating')
    desserts_serializer = ItemSerializer(desserts, many=True)

    return Response([meals, starters_serializer.data, desserts_serializer.data])


def get_half_course_curry_combs(items, money):
    half_courses = items.filter(category='half course').order_by('rating')
    curries = items.filter(category='curry').order_by('rating')
    combs = []
    for half_course in half_courses:
        rem_money = money - half_course.price
        possible_curries = curries.filter(price__lte=rem_money)
        for pos_cur in possible_curries:
            combs.append({'bread': half_course, 'curry': pos_cur})
    return combs
