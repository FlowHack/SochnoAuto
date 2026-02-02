from django.db import models


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
