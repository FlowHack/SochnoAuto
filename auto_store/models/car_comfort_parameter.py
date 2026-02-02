from django.db import models

from .car import Car


class CarComfortParameter(models.Model):
    car = models.ForeignKey(
        Car,
        related_name='car_comfort_parameter',
        on_delete=models.CASCADE
    )
    key = models.CharField(
        'Параметр',
        max_length=50,
    )
    value = models.TextField('Значение')

    class Meta:
        ordering = ['key']
        unique_together = ('car', 'key')

    def __str__(self):
        return f"{self.key} для {self.car.brand} {self.car.car_model}"
