from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_cleanup import cleanup


class Feedback(models.Model):
    name_user = models.CharField(
        'Имя пользователя',
        max_length=200,
    )
    feedback = models.TextField(
        'Отзыв пользователя',
        null=True,
    )
    answer = models.TextField(
        'Ответ компании',
        null=True,
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True,
    )
    item_object = models.CharField(
        'Объект оценки',
        null=True,
        max_length=250,
    )
    date_create = models.DateTimeField(
        'Дата добавления отзыва'
    )

    class Meta:
        ordering = ['date_create']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        feedback = self.feedback
        feedback = f'{feedback[0:15]}...' if len(feedback) > 15 else feedback
        return f'{self.name_user}: {feedback}'


@cleanup.select
class HomepageImage(models.Model):
    image = models.ImageField(upload_to='uploads/homepage_image/')
    order_image = models.PositiveIntegerField(
        'Порядок картинки',
        default=0,
        blank=False,
        null=False
    )
    caption = models.CharField(
        'Описание картинки',
        max_length=200,
        blank=True
    )

    class Meta:
        ordering = ['order_image']
        verbose_name = 'Картинка стартовой страницы'
        verbose_name_plural = 'Картинки для стратовой страницы'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_image:
            self.order_image = self.objects.count()
            super().save(*args, **kwargs)
