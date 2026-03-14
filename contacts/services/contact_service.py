import logging
from typing import Any

from django.db.models import Q
from django.utils import timezone

from cars.models import Car
from contacts.models import RequestContact

from .email_service import EmailContactService

logger = logging.getLogger(__name__)


class ContactService:
    """Сервис для работы с заявками"""

    class ExpiresAtOverdue(Exception):
        """Класс ошибки в случае, если истек срок действия токена"""

        pass

    @staticmethod
    def check_duplicate_request(
        type_request: str,
        name: str,
        email: str,
        car: Car | None = None
    ) -> bool:
        """Проверяет существует ли такая же заявка в БД

        Args:
            type_request (str): Тип заявки
            name (str): Имя клиента
            email (str): E-Mail клиента
            car (Car | None, optional): Объект автомобиля, если он необходим
                в заявке. Defaults to None.

        Returns:
            bool: Существует ли такая заявка в БД
        """

        filters = Q(
            type_request=type_request,
            name=name,
            email=email,
            expires_at__gt=timezone.now()
        )

        if car:
            filters &= Q(car=car)
        else:
            filters &= Q(car__isnull=True)

        return RequestContact.objects.filter(filters).exclude(
            status=RequestContact.Status.COMPLETE
        ).exists()

    @staticmethod
    def get_car_by_slug(car_slug: str) -> Car | None:
        """Получает объект автомобиля по SlugField

        Args:
            car_slug (str): Slug искомой модели

        Returns:
            Car | None: Модель автомобиля, если он есть в БД,
                иначе None
        """

        try:
            return Car.objects.get(slug=car_slug)
        except Car.DoesNotExist:
            return None

    @staticmethod
    def create_request_contact(form_data: dict[str, Any]) -> RequestContact:
        """Создает новую заявку в БД

        Args:
            form_data (dict[str, Any]): Словарь с параметрами заявки

        Returns:
            RequestContact: Объект созданной заявки
        """

        return RequestContact.objects.create(
            name=form_data['name'],
            email=form_data['email'],
            telephone_number=form_data['telephone_number'],
            type_request=form_data['type_request'],
            status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION,
            car=form_data.get('car')
        )

    @staticmethod
    def confirm_email(token) -> RequestContact | None:
        """Подтверждает почту для заявки

        Args:
            token (_type_): Токен заявки

        Raises:
            ContactService.ExpiresAtOverdue: Ошибка истекшего срока
                действия для токена

        Returns:
            RequestContact | None: Объект заявки, если она существует,
                иначе None
        """

        try:
            request_contact = RequestContact.objects.get(
                token=token,
                status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION,
            )
        except RequestContact.DoesNotExist as e:
            logger.error(f'Записи с токеном {token} не существует: {e}')
            return None

        if request_contact.expires_at < timezone.now():
            raise ContactService.ExpiresAtOverdue('Истек срок действия токена')

        request_contact.status = RequestContact.Status.EMAIL_CONFIRMED
        request_contact.confirmed_at = timezone.now()
        request_contact.save()
        return request_contact

    @staticmethod
    def refresh_token(token: str, request) -> None:
        """Обновляет токен

        Args:
            token (str): Токен
        """

        try:
            request_contact = RequestContact.objects.get(
                token=token
            )
        except RequestContact.DoesNotExist as e:
            logger.error(f'Записи с токеном {token} не существует: {e}')
            return

        request_contact.new_token()

        EmailContactService().send_confirmation_message(
            request_contact, request
        )
        logger.info(
            f'Для заявки #{request_contact.id} создан новый токен: '
            f'{request_contact.token}'
        )

    @staticmethod
    def send_autoteka(request_contact, request):
        EmailContactService().send_autoteka(request_contact, request)
        request_contact.status = RequestContact.Status.COMPLETE
        request_contact.complete_at = timezone.now()
        request_contact.save()
