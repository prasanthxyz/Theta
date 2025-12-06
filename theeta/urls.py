from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from food_suggestion import urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'theeta.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    path("admin/", admin.site.urls),
    path("", include(urls.urlpatterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
