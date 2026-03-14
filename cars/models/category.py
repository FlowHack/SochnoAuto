from django.db import models
from django.utils.text import slugify
from django_cleanup import cleanup


@cleanup.select
class CarCategory(models.Model):
    name = models.CharField(
        'Наименование категории',
        max_length=30,
        unique=True,
        help_text='Тип автомобиля: Легковой, Грузовой и т.д.'
    )
    image = models.ImageField(
        upload_to='uploads/category_image/',
        help_text='Иконка категории (рекомендуемый размер 64х64 px)'
    )
    slug = models.SlugField(
        'Slug',
        max_length=25,
        unique=True,
        blank=True,
        editable=False
    )
    order_category = models.PositiveIntegerField(
        'Порядок категории в выдаче',
    )

    class Meta:
        ordering = ['order_category']
        verbose_name = 'Категория автомобиля'
        verbose_name_plural = 'Категория автомобилей'

    def save(self, *args, **kwargs):
        if not self.slug or self.name_changed():
            self.slug = slugify(self.name, allow_unicode=True)

        super().save(*args, **kwargs)

    def name_changed(self):
        """Проверка, было ли изменено поле name"""

        if self.pk:
            try:
                old_obj = CarCategory.objects.get(pk=self.pk)
                return old_obj.name == self.name
            except CarCategory.DoesNotExist:
                return True
        return True

    def __str__(self):
        return self.name
