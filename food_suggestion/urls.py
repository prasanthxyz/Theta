from django.conf.urls import url
from food_suggestion import views

urlpatterns = [
    # Examples:
    url(r'^get_all_items/$', views.get_all_items, name='all_items'),
    url(r'^get_all_hotels/$', views.get_all_hotels, name='all_hotels'),
    url(r'^get_item/(?P<item_id>\d+)/$', views.get_item, name='item'),
    url(r'^get_suggestions/(?P<hotel>\w+)/(?P<money>\w+)/(?P<people>\d+)/(?P<option>\d+)/(?P<veg>\w+)/$', views.get_suggestions, name='item'),
    url(r'^upload/$', views.upload, name='upload')
]
