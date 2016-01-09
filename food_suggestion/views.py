from django.shortcuts import render

from food_suggestion.serializers import ItemSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from food_suggestion.models import Item


@api_view(['GET', 'POST'])
def get_all_items(request):
    if request.method == 'GET':
        s = Item.objects.all()
        ser = ItemSerializer(s, many=True)
        return Response(ser.data)
    elif request.method == 'POST':
        ser = ItemSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def get_item(request, item_id):
    if request.method == 'GET':
        item = Item.objects.get(pk=item_id)
        ser = ItemSerializer(item)
        return Response(ser.data)
    elif request.method == 'PATCH':
        item = Item.objects.get(pk=item_id)
        ser = ItemSerializer(item, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)