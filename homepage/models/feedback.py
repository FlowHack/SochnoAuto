from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Feedback(models.Model):
    """Модель отзыва с Авито"""

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
    avatar = models.URLField(
        'Ссылка на аватар',
        max_length=200,
        null=True
    )

    class Meta:
        ordering = ['date_create']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        feedback = (
            f'{self.feedback[0:15]}...'
            if len(self.feedback) > 15 else self.feedback
        )
        return f'{self.name_user}: {feedback}'
