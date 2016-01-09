from django.conf.urls import include, url

urlpatterns = [
    # Examples:
    url(r'^get_all_items/$', 'food_suggestion.views.get_all_items', name='all_items'),
    url(r'^get_item/(?P<item_id>\d+)/$', 'food_suggestion.views.get_item', name='item'),
]
