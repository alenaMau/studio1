from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.static import serve
from django.conf.urls.static import static


urlpatterns = [
   path('superadmin/', admin.site.urls, name='superadmin'),
   path('catalog/', include('catalog.urls'))
]


if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

