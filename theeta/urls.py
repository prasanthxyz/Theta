from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from food_suggestion import urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'theeta.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^', include(urls.urlpatterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
