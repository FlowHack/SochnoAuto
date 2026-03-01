import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from cars.models import Car


class RequestContact(models.Model):
    """Модель запроса к компании"""

    class Status(models.TextChoices):
        """Статус заявки"""

        WAIT_EMAIL_CONFIRMATION = (
            'wait_email_CONFIRMATION', 'Ждет потверждения E-mail'
        )
        EMAIL_CONFIRMED = 'email_confirmed', 'E-mail подтвержден'
        WORK = 'work', 'В работе'
        COMPLETE = 'complete', 'Отработано'

    class TypeRequest(models.TextChoices):
        """Тип заявки"""

        AUTOTEKA = 'autoteka', 'Автотека'
        CONTACT_US = 'contact_us', 'Связаться с нами'
        CONTACT_CAR = 'contact_car', 'Связаться по автомобилю'

    token = models.UUIDField(
        'Токен подтверждения почты',
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(
        'Имя клиента',
        max_length=100
    )
    email = models.EmailField('E-MAIL пользователя')
    telephone_number = models.CharField(
        'Номер телефона клиента',
        max_length=15
    )
    type_request = models.CharField(
        'Тип заявки',
        choices=TypeRequest.choices
    )
    status = models.CharField(
        'Статус заявки',
        choices=Status.choices
    )
    car = models.ForeignKey(
        Car,
        models.CASCADE,
        related_name='leads',
        verbose_name='Автомобиль',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        'Дата создания заявки',
        auto_now_add=True
    )
    expires_at = models.DateTimeField(
        'Дата окончания срока токена'
    )
    confirmed_at = models.DateTimeField(
        'Дата подтверждения заявки',
        blank=True, null=True
    )
    complete_at = models.DateTimeField(
        'Дата выполнения заявки',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Заявка клиента'
        verbose_name_plural = 'Заявки клиента'
        indexes = [
            models.Index(fields=['status', 'expires_at']),
            models.Index(fields=['token'])
        ]

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.expires_at = timezone.now() + settings.LIFETIME_TOKEN_CONTACTS
        super().save(*args, **kwargs)

    def is_expired(self):
        """Функция определения истек ли срок жизни токена"""

        return (
            self.status == self.Status.WAIT_EMAIL_CONFIRMATION and
            timezone.now() > self.expires_at
        )

    def new_token(self):
        """Функция генерирует новый токен"""

        self.token = uuid.uuid4()
        self.expires_at = timezone.now() + settings.LIFETIME_TOKEN_CONTACTS
        self.save()

        return self.token
