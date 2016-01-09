from rest_framework import serializers
from food_suggestion.models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'hotel_name', 'name', 'rating', 'price', 'category', 'veg')


class HalfCourseCombSerializer(serializers.Serializer):
    bread = ItemSerializer()
    curry = ItemSerializer()
