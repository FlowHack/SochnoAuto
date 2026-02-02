from django.db import models
from django.utils.text import slugify


class CarCategory(models.Model):
    name = models.CharField(
        'Наименование категории',
        max_length=30,
        unique=True
    )
    slug = models.SlugField(
        'Slug', max_length=25
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
