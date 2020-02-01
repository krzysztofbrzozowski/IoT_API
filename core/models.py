from django.db import models
from datetime import datetime


class Sensor(models.Model):
    mac_address = models.CharField(max_length=17)
    sensor_name = models.CharField(max_length=100)
    read_auth = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.mac_address} - {self.sensor_name}'


class TempReading(models.Model):
    title = models.AutoField(primary_key=True)
    mac_address = models.CharField(max_length=17)
    sensor_name = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)

    temperature = models.FloatField()
    humidity = models.FloatField(null=True)
    pressure = models.FloatField(null=True)
    adc = models.FloatField()

    def __str__(self):
        return f'{self.title} - {self.temperature}'

    def save(self, *args, **kwargs):
        queryset = Sensor.objects.filter(mac_address=self.mac_address)
        if queryset:
            for instance in queryset:
                self.sensor_name = instance.sensor_name

        else:
            self.sensor_name = 'UNKNOWN_SENSOR'

        super(TempReading, self).save(*args, **kwargs)

    @classmethod
    def create_avg_read(cls, **kwargs):
        reading = TempReading()
        for k, v in kwargs.items():
            reading.__setattr__(k, v)
        return reading
