from django.db import models

class Item(models.Model):
    hotel_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)      # bread, beverage
    veg = models.BooleanField()
