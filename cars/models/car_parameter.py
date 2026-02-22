from .car import Car
from django.db import models


class CarParameter(models.Model):
    class TypeParameter(models.TextChoices):
        COMFORT = 'comfort', 'Комфорт'
        TECHNICAL = 'technical', 'Технический'
        SAFETY = 'safety', 'Безопасность'

    car = models.ForeignKey(
        Car, models.CASCADE, related_name='parameters'
    )
    type_parameter = models.CharField(
        'Тип параметра',
        max_length=15,
        help_text='Выберите к какому типу относится параметр',
        choices=TypeParameter.choices,
        default=TypeParameter.TECHNICAL
    )
    key = models.CharField(
        'Параметр',
        max_length=200,
        help_text='Укажите название параметра'
    )
    value = models.CharField(
        'Значение',
        max_length=50,
        help_text='Укажите значение для параметра'
    )
    uom = models.CharField(
        'Система исчисления',
        max_length=15, null=True, blank=True,
        help_text=(
            'Укажите систему исчисления параметра (например: шт.; л.с. и т.д.)'
        )
    )

    class Meta:
        ordering = ['key']
        unique_together = ('car', 'key')
        verbose_name = 'Параметр автомобиля'
        verbose_name_plural = 'Параметры автомобиля'

    def __str__(self):
        return f'{self.key[:15]} - {self.value} {self.uom}'
