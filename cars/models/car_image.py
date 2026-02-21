from django.core.validators import FileExtensionValidator
from django.db import models
from django_cleanup import cleanup

from .car import Car


@cleanup.select
class CarImage(models.Model):
    """Модель изображения для автомобиля"""

    car = models.ForeignKey(
        Car,
        related_name='car_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        'Изображение',
        upload_to='uploads/car_image/%Y/%m/%d/',
        help_text='Прикрепите изображение автомобиля (макс. 15мб)',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'webp'],
                message=(
                    'Разрешены только файлы изображений: JPG, JPEG, PNG, WEBP'
                )
            )
        ]
    )
    caption = models.CharField(
        'Описание картинки',
        max_length=200,
        blank=True,
        help_text='Заглушка, если картинка не загрузится'
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
