from django.db import models

class Item(models.Model):
    hotel_name = models.CharField(max_length=100)
    geolocation = models.CharField(max_length=100)