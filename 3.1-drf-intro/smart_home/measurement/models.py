from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.CharField(max_length=150, blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.name} ({self.description})"


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="measurements", verbose_name="ID датчика")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Температура")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время измерения")
    image = models.ImageField(upload_to="measurements/", blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return f"{self.sensor_id} - {self.temperature}°С ({self.created_at})"