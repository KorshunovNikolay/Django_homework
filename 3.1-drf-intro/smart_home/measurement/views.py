from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView

from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer


class SensorListCreateView(ListCreateAPIView):
    # Создание нового датчика и получение списка датчиков
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorRetrieveUpdateView(RetrieveUpdateAPIView):
    # Получение подробной информации по датчику и его обновление
    queryset = Sensor.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SensorDetailSerializer
        return SensorSerializer


class MeasurementCreateView(CreateAPIView):
    # Добавление измерения температуры
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer