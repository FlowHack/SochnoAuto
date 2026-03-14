import logging

from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import FormView

from .forms import RequestContactForm
from .models import RequestContact
from .services import ContactService, EmailContactService

logger = logging.getLogger(__name__)


class RequestContactCreateView(FormView):
    form_class = RequestContactForm

    def form_valid(self, form):
        request_contact = ContactService().create_request_contact(
            form.cleaned_data
        )

        EmailContactService().send_confirmation_message(
            request_contact, self.request
        )

        return JsonResponse(
            {
                'success': True,
                'message': 'Проверьте почту для её подтверждения!'
            }
        )

    def form_invalid(self, form):
        return JsonResponse(
            {
                'success': False,
                'errors': form.errors
            }, status=400
        )


class ConfirmEmailView(View):
    def get(self, request: HttpRequest, token: str):
        contact_service = ContactService()

        try:
            request_contact = contact_service.confirm_email(token)
        except ContactService.ExpiresAtOverdue as e:
            logger.warning(f'У токена {token} истек срок действия: {e}')

            contact_service.refresh_token(token, request)

            messages.error(
                request,
                'Срок действия ссылки истек! На Вашу почту была отправлена'
                ' новая ссылка!'
            )
            return redirect('contacts:confirm_error')

        if not request_contact:
            messages.error(request, 'Заявка не найдена!')
            return redirect('contacts:contacts')

        email_service = EmailContactService()
        email_service.send_confirmed_email(request_contact, request)

        if (
            request_contact.type_request ==
            RequestContact.TypeRequest.AUTOTEKA and
            request_contact.car.autoteka
        ):
            contact_service.send_autoteka(request_contact, request)

        messages.success(
            request,
            'Ваш email успешно подтвержден! Ваша заявка будет обработана '
            'в ближайшее время!'
        )

        return redirect('contacts:confirm_success')


def contacts(request):
    """Страница контактов."""
    return render(request, 'contacts/contacts.html')
