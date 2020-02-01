from rest_framework import serializers
from .models import TempReading


class TempReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempReading
        fields = ('title', 'mac_address', 'sensor_name',
                  'timestamp', 'temperature', 'humidity', 'pressure', 'adc')

    def to_representation(self, instance):
        representation = super(TempReadingSerializer,
                               self).to_representation(instance)
        representation['timestamp'] = instance.timestamp.strftime(
            '%d %b %Y %H:%M:%S')
        return representation
