from rest_framework import serializers
from food_suggestion.models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        # fields = ('id', 'hotel_name', 'name', 'rating', 'price', 'category', 'veg')
        fields = ('name', 'rating', 'price', 'veg')


class HotelSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class HalfCourseCombSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    # hotel_name = serializers.CharField(max_length=100)
    rating = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    veg = serializers.BooleanField()


class HalfCourseCombSerializer_backup(serializers.Serializer):
    half_course = ItemSerializer()
    curry = ItemSerializer()
