from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

from core.views import GetTimeSync, GetTimedelta, TempCreateView, TempRequestView

urlpatterns = [
    path('get-sensor-temperature/<sensor>/<timedelta>',
         TempRequestView.as_view(), name='temp-view'),

    path('', TempCreateView.as_view(), name='temp-view'),
    path('timesync', GetTimeSync.as_view(), name='time-sync'),
    path('timedelta/<delta>', GetTimedelta.as_view(), name='time-delta'),

    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
