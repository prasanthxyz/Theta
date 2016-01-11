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


def get_suggestions_helper(hotels, money, people, option, veg):
    money = int(money)
    people = int(people)
    option = int(option)

    # category
    # STARTER = 1
    # MEAL = 2
    # DESSERT = 4

    # starter, meal, dessert
    split_table = {
        1: [100, 0, 0],
        2: [0, 100, 0],
        3: [40, 60, 0],
        4: [0, 0, 100],
        5: [50, 0, 50],
        6: [0, 75, 25],
        7: [30, 50, 20]
    }

    split = split_table[option]
    starter_money = float(money * split[0]) / 100
    meal_money = float(money * split[1]) / 100
    dessert_money = float(money * split[2]) / 100

    # items = Item.objects.filter(hotel_name=hotel_name, price__lte=(money/people))
    if veg == 'true':
        items = Item.objects.filter(price__lte=(money / people), veg=True)
    else:
        items = Item.objects.filter(price__lte=(money / people))

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

    id = 1

    for hotel in hotels:
        try:
            if len(starters[hotel]) > 0:
                starter0 = starters[hotel][0]
            else:
                starter0 = None
            if len(meals[hotel]) > 0:
                meal0 = meals[hotel][0]
            else:
                meal0 = None
            if len(desserts[hotel]) > 0:
                dessert0 = desserts[hotel][0]
            else:
                dessert0 = None

            if len(starters[hotel]) > 1:
                starter1 = starters[hotel][1]
            else:
                starter1 = None
            if len(meals[hotel]) > 1:
                meal1 = meals[hotel][1]
            else:
                meal1 = None
            if len(desserts[hotel]) > 1:
                dessert1 = desserts[hotel][1]
            else:
                dessert1 = None

            if option == 1:
                id += 1
                append_suggestions(suggestions, id, hotel, starter0, None, None)
                id += 1
                append_suggestions(suggestions, id, hotel, starter1, None, None)
            elif option == 2:
                id += 1
                append_suggestions(suggestions, id, hotel, None, meal0, None)
                id += 1
                append_suggestions(suggestions, id, hotel, None, meal1, None)
            elif option == 4:
                id += 1
                append_suggestions(suggestions, id, hotel, None, None, dessert0)
                id += 1
                append_suggestions(suggestions, id, hotel, None, None, dessert1)
            elif option == 3:
                id += 1
                append_suggestions(suggestions, id, hotel, starter0, meal0, None)
                id += 1
                append_suggestions(suggestions, id, hotel, starter1, meal0, None)
                id += 1
                append_suggestions(suggestions, id, hotel, starter0, meal1, None)
                id += 1
                append_suggestions(suggestions, id, hotel, starter1, meal1, None)
            elif option == 5:
                id += 1
                append_suggestions(suggestions, id, hotel, starter0, None, dessert0)
                id += 1
                append_suggestions(suggestions, id, hotel, starter1, None, dessert0)
                id += 1
                append_suggestions(suggestions, id, hotel, starter0, None, dessert1)
                id += 1
                append_suggestions(suggestions, id, hotel, starter1, None, dessert1)
            elif option == 6:
                id += 1
                append_suggestions(suggestions, id, hotel, None, meal0, dessert0)
                id += 1
                append_suggestions(suggestions, id, hotel, None, meal1, dessert0)
                id += 1
                append_suggestions(suggestions, id, hotel, None, meal0, dessert1)
                id += 1
                append_suggestions(suggestions, id, hotel, None, meal1, dessert1)
            else:
                id += 1
                append_suggestions(suggestions, id, hotel, starter0, meal0, dessert0)
                id += 1
                append_suggestions(suggestions, id, hotel, starter1, meal0, dessert0)
                id += 1
                append_suggestions(suggestions, id, hotel, starter0, meal1, dessert0)
                id += 1
                append_suggestions(suggestions, id, hotel, starter0, meal0, dessert1)
        except IndexError:
            continue

    suggestions = sorted(suggestions, key=lambda x: x["rating"], reverse=True)

    return Response(suggestions[:10])


def append_suggestions(suggestions, id, hotel, starter, meal, dessert, img_id=''):
    import random
    img_id = int(random.random() * 10) % 4 + 1
    if img_id == '':
        thumb = 'img/cover.jpg'
    else:
        thumb = 'http://theta-appl.azurewebsites.net/static/' + str(img_id) + '.jpg'
    dishes = []
    price1 = 0
    price2 = 0
    price3 = 0
    rating1 = 0
    rating2 = 0
    rating3 = 0
    veg1 = True
    veg2 = True
    veg3 = True
    if starter:
        dishes.append(starter['name'])
        price1 += float(starter['price'])
        rating1 += (starter['rating'])
        veg1 = starter['veg']
    if meal:
        dishes.append(meal['name'])
        price2 += float(meal['price'])
        rating2 += (meal['rating'])
        veg2 = meal['veg']
    if dessert:
        dishes.append(dessert['name'])
        price3 += float(dessert['price'])
        rating3 += (dessert['rating'])
        veg3 = dessert['veg']
    if len(dishes) > 0:
        suggestions.append(
                {
                    "id": id,
                    "hotel": hotel,
                    "dishes": dishes,
                    "cost": (price1 + price2 + price3),
                    "rating": (rating1 + rating2 + rating3),
                    "veg": (veg1 & veg2 & veg3),
                    "thumb": thumb
                }
        )


@api_view(['GET'])
def get_suggestions(request, hotel, money, people, option, veg):
    if hotel == 'any':
        hotels = list(get_all_hotels_list())
    else:
        hotels = [hotel]
    return get_suggestions_helper(hotels, money, people, option, veg)


def get_half_course_curry_combs(items, money, hotel):
    half_courses = items.filter(category='half course', hotel_name=hotel).order_by('-rating')
    curries = items.filter(category='curry', hotel_name=hotel).order_by('-rating')
    combs = []
    for half_course in half_courses:
        rem_money = money - float(half_course.price)
        possible_curries = curries.filter(price__lte=rem_money)
        for pos_cur in possible_curries:
            combs.append({'half_course': half_course, 'curry': pos_cur})
    meals = []
    for comb in combs:
        meals.append({'name': comb['half_course'].name + ' and ' + comb['curry'].name,
                      'price': comb['half_course'].price + comb['curry'].price,
                      'rating': (comb['half_course'].rating + comb['curry'].rating) / 2,
                      'veg': (comb['half_course'].veg & comb['curry'].veg)
                      })
    return meals


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import csv
import sys
from random import random


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        formdata = request.POST.get('db').strip()
        rows = []
        for row in formdata.split('\n'):
            rows.append(row.split(','))
        from food_suggestion.models import Item
        hotels = ['The Beatle, Hiranandani', 'Gurukripa', 'Sigree Global Grill', 'Mehman Nawazi', 'Mirchi And Mime']

        reader = rows
        for hotel in hotels:
            for record in reader:
                # hotel_name = record['hotel_name']
                hotel_name = hotel
                name = record[0]
                # rating = record['rating']
                rating = int(random() * 1000) % 6
                price = int(record[1]) + (int(random() * 100) % 10 - 5)
                category = record[2]
                veg = False if record[3].strip() == '0' else True
                Item(hotel_name=hotel_name,
                     name=name,
                     rating=rating,
                     price=price,
                     category=category,
                     veg=veg).save()
        return HttpResponse('done')
    else:
        return HttpResponse(
            "<form method='post'><textarea name='db'> </textarea><button type='submit' value='submit'>Submit</button></form>")


def get_half_course_curry_combs_temp(items, money, hotel):
    half_courses = items.filter(category='half course', hotel_name=hotel).order_by('-rating')
    curries = items.filter(category='curry', hotel_name=hotel).order_by('-rating')
    combs = []
    for half_course in half_courses:
        rem_money = money - float(half_course.price)
        possible_curries = curries.filter(price__lte=rem_money)
        for pos_cur in possible_curries:
            combs.append({'half_course': half_course, 'curry': pos_cur})
    return combs
