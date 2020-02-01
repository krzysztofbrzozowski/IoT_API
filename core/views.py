from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Avg

from rest_framework.renderers import JSONRenderer
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework_json_api.renderers import JsonApiRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .serializers import TempReadingSerializer
from .models import Sensor, TempReading

import datetime


class GetTimeSync(APIView):
    def get(self, request, *args, **kwargs):
        datetime_now = datetime.datetime.now()
        message = {
            'datetime_now': (int(datetime_now.year), int(datetime_now.month), int(datetime_now.day), int(datetime_now.weekday()),
                             int(datetime_now.hour), int(datetime_now.minute), int(datetime_now.second), 0),
        }
        return Response(message)


class GetTimedelta(APIView):
    def get(self, request, *args, **kwargs):
        delta = int(self.kwargs['delta'])

        # SECONDS
        if delta < 60:
            requested_datetime = datetime.datetime.now() - datetime.timedelta(seconds=delta)
        # MINUTES
        if delta > 59:
            requested_datetime = datetime.datetime.now() - datetime.timedelta(minutes=delta/60)
        # HOURS
        if delta > (59 * 60):
            requested_datetime = datetime.datetime.now(
            ) - datetime.timedelta(hours=delta/(60 * 60))
        # DAYS
        if delta > (23 * 60 * 60):
            requested_datetime = datetime.datetime.now(
            ) - datetime.timedelta(days=delta/(24 * 60 * 60))

        message = {
            'timestamp': requested_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        }
        return Response(message)


class TempCreateView(mixins.ListModelMixin, generics.CreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = TempReadingSerializer

    def get(self, request, *args, **kwargs):
        return render(request, 'core/index.html', {})

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TempRequestView(mixins.ListModelMixin, generics.CreateAPIView):
    # class TempRequestView(generics.ListAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = TempReadingSerializer
    # renderer_classes = JSONRenderer

    def get(self, request, *args, **kwargs):
        sensor = self.kwargs['sensor']
        timedelta = int(self.kwargs['timedelta'])

        sensor_a = Sensor.objects.filter(
            sensor_name=sensor, read_auth=True) if self.request.auth else None

        sensor_u = Sensor.objects.filter(
            sensor_name=sensor, read_auth=False)

        if timedelta == 1:
            delta = datetime.datetime.now() - datetime.timedelta(days=timedelta)

            if sensor_a or sensor_u:
                qs = TempReading.objects.filter(
                    timestamp__gte=delta, sensor_name=sensor).order_by('timestamp')
                serializer = TempReadingSerializer(qs, many=True)
                return Response(serializer.data)

            else:
                return Response({'message': 'you are NOT authorized to read this sensor'})

        if timedelta == 10:
            if sensor_a or sensor_u:
                qs = set()
                for n in range(0, timedelta):
                    dtn = datetime.datetime.now()
                    dt = datetime.datetime
                    mdt = dtn - (dt(dtn.year, dtn.month, dtn.day, 0,
                                    0, 0) - datetime.timedelta(days=n))

                    delta = dtn - mdt

                    avg_temp = TempReading.objects.filter(
                        timestamp__gte=delta, sensor_name=sensor).aggregate(Avg('temperature'))
                    avg_humidity = TempReading.objects.filter(
                        timestamp__gte=delta, sensor_name=sensor).aggregate(Avg('humidity'))
                    avg_pressure = TempReading.objects.filter(
                        timestamp__gte=delta, sensor_name=sensor).aggregate(Avg('pressure'))

                    qs_obj = TempReading.create_avg_read(
                        title=n,
                        sensor_name=sensor,
                        timestamp=delta,
                        temperature=round(avg_temp['temperature__avg'], 2),
                        humidity=round(avg_humidity['humidity__avg'], 2),
                        pressure=round(avg_pressure['pressure__avg'], 2))

                    qs.add(qs_obj)

                serializer = TempReadingSerializer(qs, many=True)
                return Response(serializer.data)

            else:
                return Response({'message': 'you are NOT authorized to read this sensor'})
