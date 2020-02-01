from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.contrib import admin

from .models import Sensor, TempReading


admin.site.register(Sensor)


@admin.register(TempReading)
class TempAdmin(admin.ModelAdmin):
    list_display = ('title', 'mac_address', 'sensor_name',
                    'timestamp', 'temperature', 'humidity', 'pressure')
    list_filter = (
        ('timestamp', DateRangeFilter), ('timestamp', DateTimeRangeFilter),
        'mac_address',
        'sensor_name',
    )
