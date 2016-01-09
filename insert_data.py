import os
import csv
import sys
from random import random


sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'theeta.settings'

from food_suggestion.models import Item


hotels = ['Ahotel', 'Bhotel', 'Chotel', 'Dhotel', 'Ehotel']

for hotel in hotels:
    reader = csv.DictReader(open('data.csv', 'rb'))
    for record in reader:
        # hotel_name = record['hotel_name']
        hotel_name = hotel
        name = record['name']
        # rating = record['rating']
        rating = int(random()*1000)%6
        price = int(record['price']) + (int(random()*100)%10 - 5)
        category = record['category']
        veg = True
        Item(hotel_name=hotel_name,
                name=name,
                rating=rating,
                price=price,
                category=category,
                veg=veg).save()

