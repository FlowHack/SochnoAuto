from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from .car_category import CarCategory


class Car(models.Model):
    class FuelTypes(models.TextChoices):
        GASOLINE = 'gasoline', 'Бензин'
        DIESEL = 'diesel', 'Дизель'
        ELECTRIC = 'electric', 'Электро'
        HYBRID = 'hybrid', 'Гибрид'
        HYDROGEN = 'hydrogen', 'Водород'
        LPG = 'lpg', 'СНГ (пропан-бутан)'

    brand = models.CharField(
        'Марка',
        max_length=50
    )
    car_model = models.CharField(
        'Модель',
        max_length=50
    )
    year_release = models.DateField(
        'Год выпуска'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    mileage = models.IntegerField(
        'Пробег',
    )
    fuel_type = models.CharField(
        'Тип топлива',
        max_length=10,
        choices=FuelTypes.choices,
        default=FuelTypes.GASOLINE
    )
    price = models.PositiveIntegerField(
        'Стоимость автомобиля в рублях',
        default=0
    )
    sold = models.BooleanField(
        'Машина продана',
        default=False
    )
    category = models.ForeignKey(
        CarCategory,
        related_name='cars_in_category',
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )
    slug = models.SlugField(
        'Slug',
        max_length=200,
        unique=True,
        blank=True,
        editable=False
    )
    is_special_offer = models.BooleanField(
        'Специальное предложение',
        default=False
    )
    date_is_special_offer = models.DateTimeField(
        'Дата когда автомобиль стал специальным предложением',
        blank=True,
        null=True
    )
    description = CKEditor5Field(
        'Описание автомобиля',
        config_name='default',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = (
                slugify(
                    f'{self.brand}-{self.car_model}-{self.id}',
                    allow_unicode=True
                )
            )
            super().save(*args, **kwargs)

    def get_year_release(self):
        return self.year_release.year

    def __str__(self):
        return (
            f'{self.brand} {self.car_model} - '
            f'{self.year_release} - {self.mileage}'
        )
