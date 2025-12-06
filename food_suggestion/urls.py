from django.urls import re_path

from food_suggestion import views

urlpatterns = [
    # Examples:
    re_path(r"^get_all_items/$", views.get_all_items, name="all_items"),
    re_path(r"^get_all_hotels/$", views.get_all_hotels, name="all_hotels"),
    re_path(r"^get_item/(?P<item_id>\d+)/$", views.get_item, name="item"),
    re_path(
        r"^get_suggestions/(?P<hotel>\w+)/(?P<money>\w+)/(?P<people>\d+)/(?P<option>\d+)/(?P<veg>\w+)/$",
        views.get_suggestions,
        name="item",
    ),
    re_path(r"^upload/$", views.upload, name="upload"),
]
