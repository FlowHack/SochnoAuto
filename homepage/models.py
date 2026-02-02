from django.db import models
from django_cleanup import cleanup


class Feedback(models.Model):
    name_user = models.CharField(
        'Имя пользователя',
        max_length=200,
    )
    feedback = models.TextField(
        'Отзыв пользователя'
    )
    answer = models.TextField(
        'Ответ компании',
        blank=True
    )

    def __str__(self):
        feedback = self.feedback
        feedback = f'{feedback[0:15]}...' if feedback.len() > 15 else feedback
        return f'{self.name_user}: {feedback}'


@cleanup.select
class HomepageImage(models.Model):
    image = models.ImageField(upload_to='uploads/homepage_image/')
    caption = models.CharField(
        'Описание картинки',
        max_length=200,
        blank=True
    )

    class Meta:
        verbose_name = 'Картинка стартовой страницы'
        verbose_name_plural = 'Картинки для стратовой страницы'
