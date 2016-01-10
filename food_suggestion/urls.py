from django.conf.urls import url

urlpatterns = [
    # Examples:
    url(r'^get_all_items/$', 'food_suggestion.views.get_all_items', name='all_items'),
    url(r'^get_all_hotels/$', 'food_suggestion.views.get_all_hotels', name='all_hotels'),
    url(r'^get_item/(?P<item_id>\d+)/$', 'food_suggestion.views.get_item', name='item'),
    url(r'^get_suggestions/(?P<money>\w+)/(?P<people>\d+)/(?P<option>\d+)/$',
        'food_suggestion.views.get_suggestions', name='item'),
    url(r'^get_suggestions/(?P<hotel>\w+)/(?P<money>\w+)/(?P<people>\d+)/(?P<option>\d+)/$',
        'food_suggestion.views.get_suggestions_for_hotel', name='item'),
]
