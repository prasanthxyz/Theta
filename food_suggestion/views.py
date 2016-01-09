from food_suggestion.serializers import ItemSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from food_suggestion.models import Item


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
def get_suggestions(request, hotel_name, money, people):
    items = Item.objects.filter(hotel_name=hotel_name)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)