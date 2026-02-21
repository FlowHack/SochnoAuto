from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from .category import CarCategory


class Car(models.Model):
    """Класс модели автомобиля"""

    class FuelTypes(models.TextChoices):
        """Варианты выбора типа топлива"""

        GASOLINE = 'gasoline', 'Бензин'
        DIESEL = 'diesel', 'Дизель'
        ELECTRIC = 'electric', 'Электро'
        HYBRID = 'hybrid', 'Гибрид'
        HYDROGEN = 'hydrogen', 'Водород'
        LPG = 'lpg', 'СНГ (пропан-бутан)'

    brand = models.CharField(
        'Бренд',
        max_length=50,
        help_text='Укажите бренд, выпускающий автомобиль',
        db_index=True
    )
    model = models.CharField(
        'Модель',
        max_length=50,
        help_text='Укажите модель автомобиля'
    )
    year_release = models.PositiveIntegerField(
        'Год выпуска',
        validators=[
            MinValueValidator(1886),  # 1886 - год создания первого автомобиля
            MaxValueValidator(date.today().year + 1)
        ],
        help_text='Укажите год выпуска автомобиля'
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=True
    )
    mileage = models.PositiveIntegerField(
        'Пробег', db_index=True,
        help_text='Укажите пробег автомобиля в километрах'
    )
    fuel_type = models.CharField(
        'Тип топлива',
        max_length=10,
        choices=FuelTypes.choices,
        default=FuelTypes.GASOLINE,
        help_text='Выберите тип топлива, если бензин - оставьте пустым'
    )
    power_hp = models.PositiveIntegerField(
        'Мощность автомобиля',
        blank=True,
        null=True,
        help_text='Укажите мощность автомобиля в л.с или кВт/ч'
    )
    color = models.CharField(
        'Цвет кузова',
        max_length=30,
        blank=True,
        help_text='Укажите цвет кузова автомобиля'
    )
    price = models.PositiveIntegerField(
        'Стоимость автомобиля в рублях',
        default=0, db_index=True
    )
    sold = models.BooleanField(
        'Машина продана',
        default=False,
        help_text='Укажите, продана ли машина'
    )
    category = models.ForeignKey(
        CarCategory,
        related_name='cars_in_category',
        on_delete=models.CASCADE,
        verbose_name='Категория',
        help_text='Выберите категорию автомобиля'
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
        default=False,
        help_text='Является ли автомобиль специальным предложением'
    )
    date_is_special_offer = models.DateTimeField(
        'Дата, когда автомобиль стал специальным предложением',
        blank=True,
        null=True
    )
    description = CKEditor5Field(
        'Описание автомобиля',
        config_name='default',
        blank=True,
        null=True,
        help_text='Напишите описание автомобиля'
    )

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def save(self, *args, **kwargs):
        if self.is_special_offer and not self.date_is_special_offer:
            self.date_is_special_offer = timezone.now()
        elif not self.is_special_offer:
            self.date_is_special_offer = None

        created = not self.pk
        super().save(*args, **kwargs)

        if created or not self.slug:
            self.slug = (
                slugify(
                    f'{self.brand}-{self.model}-{self.id}',
                    allow_unicode=True
                )
            )
            super().save(update_fields=['slug'], *args, **kwargs)

    def __str__(self):
        status = "🔴 ПРОДАНО" if self.sold else "🟢 В продаже"
        return (
            f'{self.brand} {self.model} ({self.year_release}) - '
            f'{self.mileage:,} км {status}'
        )

    @property
    def full_name(self):
        """Полное название для ссылок"""

        return f"{self.brand} {self.model} {self.year_release.year}"
