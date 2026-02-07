from django.db import models
from django.utils.text import slugify
from django_cleanup import cleanup


@cleanup.select
class CarCategory(models.Model):
    name = models.CharField(
        'Наименование категории',
        max_length=30,
        unique=True,
    )
    image = models.ImageField(upload_to='uploads/category_image/')
    slug = models.SlugField(
        'Slug',
        max_length=25,
        unique=True,
        blank=True,
        editable=False
    )
    order_category = models.PositiveIntegerField(
        'Сортировка категорий',
    )

    class Meta:
        ordering = ['order_category']
        verbose_name = 'Категория автомобиля'
        verbose_name_plural = 'Категория автомобилей'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
            print(self.slug)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
