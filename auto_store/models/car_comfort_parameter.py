from django.db import models

from .car import Car


class CarComfortParameter(models.Model):
    car = models.ForeignKey(
        Car,
        related_name='comfort_parameters',
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
        verbose_name = 'Параметр комфорта'
        verbose_name_plural = 'Параметры комфорта'

    def __str__(self):
        return f"{self.key} для {self.car.brand} {self.car.car_model}"
