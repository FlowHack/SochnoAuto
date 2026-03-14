import email.utils
import logging
from email.message import MIMEPart

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpRequest
from django.template.loader import render_to_string

from contacts.models import RequestContact

logger = logging.getLogger(__name__)


class EmailContactService:
    """Обработка отправки писем"""

    template_confirmation = 'contacts/emails/confirmation.html'
    template_text_confirmation = 'contacts/emails/text/confirmation.txt'
    template_confirmed = 'contacts/emails/confirmed.html'
    template_autoteka = 'contacts/emails/autoteka.html'
    template_text_autoteka = 'contacts/emails/text/autoteka.txt'
    template_autoteka_sended = 'contacts/emails/autoteka_sended.html'

    def send_confirmation_message(
        self, lead: RequestContact, request: HttpRequest
    ):
        """Отправка письма с ссылкой на подтверждение почты

        Args:
            lead (Lead): Объект заявки
            request (HttpRequest): Объект запроса
        """

        try:
            image_logo, cid = self._get_image_logo_for_email()
            html_email = self._get_html_confirmation_email(lead, request, cid)
            text = self._get_text_confirmation_email(lead, request)

            msg = EmailMultiAlternatives(
                'Подтверждение заявки | СОЧНО АВТО',
                text,
                settings.EMAIL_HOST_USER,
                [lead.email]
            )
            msg.attach_alternative(html_email, 'text/html')
            msg.attach(image_logo)
            msg.send()
            logger.info(
                f'Ссылка для подтверждения отправлена по заявке #{lead.id}'
            )
        except Exception as e:
            logger.error(
                f'При отправке ссылки подтверждения на {lead.email} произошла '
                f'ошибка: {e}'
            )

    @staticmethod
    def _get_image_logo_for_email() -> tuple[MIMEPart, str]:
        """Получает картинку логотипа компании

        Returns:
            tuple[MIMEPart, str]: (Объект картинки, cid по которому можно
                вставить картинку в html)
        """

        logo_path = settings.STATICFILES_DIRS[0] / 'favicon.png'

        with open(logo_path, 'rb') as f:
            logo_data = f.read()

        image_logo_cid = email.utils.make_msgid()
        image_logo_email = MIMEPart()
        image_logo_email.set_content(
            logo_data,
            maintype='image',
            subtype='png',
            disposition='inline',
            cid=image_logo_cid
        )

        return image_logo_email, image_logo_cid[1:-1]

    def _get_html_confirmation_email(
        self, lead: RequestContact, request: HttpRequest, cid: str
    ) -> str:
        """Собирает HTML письма для подтверждения почты

        Args:
            lead (Lead): Объект заявки
            request (HttpRequest): Объект запроса
            cid (str): cid иконки компании для использовани в шаблоне

        Returns:
            str: HTML строку письма
        """

        return render_to_string(
            self.template_confirmation,
            {
                'lead': lead,
                'cid': cid
            },
            request
        )

    def _get_text_confirmation_email(
        self, lead: RequestContact, request: HttpRequest
    ) -> str:
        """Собирает текстовую составляющую письма для подтверждения почты

        Args:
            lead (Lead): Объект заявки
            request (HttpRequest): Объект запроса

        Returns:
            str: HTML строку письма
        """
        return render_to_string(
            self.template_text_confirmation,
            {'lead': lead}, request
        )

    def send_confirmed_email(self, lead: RequestContact, request: HttpRequest):
        """Отправка письма сотрудникам о том, что появилась новая заявка

        Args:
            lead (Lead): Объект заявки
            request (HttpRequest): Объект запроса
        """

        try:
            image_logo, cid = self._get_image_logo_for_email()
            html_email = self._get_html_confirmed_email(lead, request, cid)

            msg = EmailMessage(
                f'✅ Подтвержденная заявка #{lead.id}',
                html_email,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_FOR
            )
            msg.content_subtype = 'html'
            msg.attach(image_logo)
            msg.send()
            logger.info(
                'Сотрудникам отправлена информацию по подтвержденной заявке '
                f'#{lead.id}'
            )
        except Exception as e:
            logger.error(
                'При отправке письма сотрудникам о новой заявке произошла '
                f'ошибка: {e}'
            )

    def _get_html_confirmed_email(
        self, lead: RequestContact, request: HttpRequest, cid: str
    ) -> str:
        """Сборка HTML письма дял сотрудников о новой заявке

        Args:
            lead (Lead): Объект заявки
            request (HttpRequest): Объект запроса
            cid (str): cid иконки компании для использовани в шаблоне

        Returns:
            str: Строковую HTML составляющую письма
        """

        return render_to_string(
            self.template_confirmed,
            {
                'lead': lead,
                'cid': cid
            },
            request
        )

    def send_autoteka(
        self, lead: RequestContact, request: HttpRequest
    ):
        """Отправка автотеки ползователю и отправка сотрудникам письма
        об отправке автотеки

        Args:
            lead (Lead): Объект заявки
            request (HttpRequest): Объект запроса
        """

        try:
            image_logo, cid = self._get_image_logo_for_email()

            text_email = self._get_text_autoteka_email(lead)
            html_email = self._get_html_autoteka_email(lead, request, cid)
            msg = EmailMultiAlternatives(
                f'📋 Автотека для {lead.car.brand} {lead.car.model}',
                text_email, settings.EMAIL_HOST_USER, [lead.email]
            )
            msg.attach_alternative(html_email, 'text/html')
            msg.attach(image_logo)
            msg.attach_file(lead.car.autoteka.path)
            msg.send()
            logger.info(f'Отправлена автотека по заявке #{lead.id}')

            html_email = self._get_html_autoteka_sended_email(
                lead, request, cid
            )
            msg_sended = EmailMessage(
                f'Отправлена автотека {lead.car.brand} {lead.car.model}',
                html_email,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_FOR
            )
            msg_sended.content_subtype = 'html'
            msg_sended.attach(image_logo)
            msg_sended.attach_file(lead.car.autoteka.path)
            msg_sended.send()
            logger.info(
                'Сотрудники предупреждены об отправленной автотеке по заявке '
                f'#{lead.id}'
            )

        except Exception as e:
            logger.error(
                f'При отправке автотеки для {lead.email} произошла ошибка: {e}'
            )

    def _get_html_autoteka_email(
        self, lead: RequestContact, request: HttpRequest, cid: str
    ) -> str:
        """Собирает HTML для письма с автотекой

        Args:
            lead (RequestContact): Объект заявки
            request (HttpRequest): Объект запроса
            cid (str): cid иконки компании для использовани в шаблоне

        Returns:
            str: Собранный HTML письма
        """

        return render_to_string(
            self.template_autoteka,
            {
                'lead': lead,
                'cid': cid
            },
            request
        )

    def _get_text_autoteka_email(self, lead: RequestContact) -> str:
        """Собирает текстовый формат письма с автотекой

        Args:
            lead (RequestContact): Объект заявки

        Returns:
            str: Собранный тект письма
        """

        return render_to_string(
            self.template_text_autoteka,
            {'lead': lead}
        )

    def _get_html_autoteka_sended_email(
        self, lead: RequestContact, request: HttpRequest, cid: str
    ) -> str:
        """Собирает HTML для письма сотрудникам о том, был отправлен файл
        автотеки

        Args:
            lead (RequestContact): Объект заявки
            request (HttpRequest): Объект запроса
            cid (str): cid иконки компании для использовани в шаблоне

        Returns:
            str: Собранный HTML для письма
        """

        return render_to_string(
            self.template_autoteka_sended,
            {
                'lead': lead,
                'cid': cid
            },
            request
        )
