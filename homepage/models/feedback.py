from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_cleanup import cleanup


@cleanup.select
class Feedback(models.Model):
    """Модель отзыва с Авито"""

    feedback_avito_id = models.PositiveIntegerField(
        'ID отзыва в Авито БД',
        unique=True
    )
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
    date_create = models.DateField(
        'Дата добавления отзыва'
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to='feedback_avatars/%Y/%m/%d/',
        max_length=500,
        null=True,
        blank=True
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

    def has_avatar(self):
        """Возвращает есть ли аватар у отзыва"""

        if self.avatar and hasattr(self.avatar, 'url'):
            return True
        return False
