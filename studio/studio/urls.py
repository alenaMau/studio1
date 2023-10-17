from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.static import serve


urlpatterns = [
   path('superadmin/', admin.site.urls, name='superadmin'),
   path('catalog/', include('catalog.urls'))
]


if settings.DEBUG:
   urlpatterns.append(path('static/<path:path>', never_cache(serve)))

