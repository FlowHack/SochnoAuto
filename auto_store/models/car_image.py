from django.db import models
from django_cleanup import cleanup

from .car import Car


@cleanup.select
class CarImage(models.Model):
    car = models.ForeignKey(
        Car,
        related_name='car_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='uploads/car_image/')
    caption = models.CharField(
        'Описание картинки',
        max_length=200,
        blank=True
    )
    order_image = models.PositiveIntegerField(
        'Порядок картинки',
        default=0,
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['order_image']
        verbose_name = 'Фотография автомобиля'
        verbose_name_plural = 'Фотографии автомобиля'
