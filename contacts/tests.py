import uuid
from datetime import timedelta
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from cars.models import Car, CarCategory


def create_car(brand, model, year_release, mileage, category, **kwargs):
    """Вспомогательная функция для создания автомобиля в тестах."""

    from django.utils.text import slugify
    count = Car.objects.count() + 1
    defaults = {
        'brand': brand,
        'model': model,
        'year_release': year_release,
        'mileage': mileage,
        'category': category,
        'slug': slugify(f'{brand}-{model}-{count}')
    }
    defaults.update(kwargs)
    car = Car(**defaults)
    car.save(force_insert=False)
    return car


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class RequestContactModelTest(TestCase):
    """Тесты для модели RequestContact"""

    def setUp(self):
        """Создание тестовых данных для заявки."""

        from contacts.models import RequestContact
        image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=image, order_category=1
        )
        self.car = create_car('Toyota', 'Camry', 2023, 10000, self.category)
        self.request = RequestContact.objects.create(
            name='Test User',
            email='test@example.com',
            telephone_number='+79000000000',
            type_request=RequestContact.TypeRequest.CONTACT_US,
            status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION,
            car=None
        )

    def test_request_contact_creation(self):
        """Тест создания заявки на обратную связь."""

        self.assertEqual(self.request.name, 'Test User')
        self.assertEqual(self.request.email, 'test@example.com')

    def test_request_contact_with_car(self):
        """Тест создания заявки с привязкой к автомобилю."""

        from contacts.models import RequestContact
        request_with_car = RequestContact.objects.create(
            name='Test User 2',
            email='test2@example.com',
            telephone_number='+79000000001',
            type_request=RequestContact.TypeRequest.CONTACT_CAR,
            status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION,
            car=self.car
        )
        self.assertEqual(request_with_car.car, self.car)

    def test_request_token_generation(self):
        """Тест генерации токена для заявки."""

        self.assertIsNotNone(self.request.token)
        self.assertIsInstance(self.request.token, uuid.UUID)

    def test_request_is_expired_false(self):
        """Тест не истечения срока заявки."""

        from django.utils import timezone

        from contacts.models import RequestContact
        request = RequestContact.objects.create(
            name='Test', email='test@example.com',
            telephone_number='+79000000000',
            type_request=RequestContact.TypeRequest.CONTACT_US,
            status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION
        )
        request.expires_at = timezone.now() + timedelta(hours=1)
        self.assertFalse(request.is_expired())

    def test_request_is_expired_true(self):
        """Тест истечения срока заявки."""

        from django.utils import timezone

        from contacts.models import RequestContact
        request = RequestContact.objects.create(
            name='Test', email='test@example.com',
            telephone_number='+79000000000',
            type_request=RequestContact.TypeRequest.CONTACT_US,
            status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION
        )
        request.expires_at = timezone.now() - timedelta(hours=1)
        self.assertTrue(request.is_expired())

    def test_request_type_choices(self):
        """Тест выбора типов заявок."""

        from contacts.models import RequestContact
        self.assertIn(
            ('autoteka', 'Автотека'), RequestContact.TypeRequest.choices
        )
        self.assertIn(
            ('contact_us', 'Связаться с нами'),
            RequestContact.TypeRequest.choices
        )

    def test_request_status_choices(self):
        """Тест выбора статусов заявок."""

        from contacts.models import RequestContact
        self.assertIn(
            ('wait_email_CONFIRMATION', 'Ждет потверждения E-mail'),
            RequestContact.Status.choices
        )
        self.assertIn(
            ('email_confirmed', 'E-mail подтвержден'),
            RequestContact.Status.choices
            )


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class RequestContactFormTest(TestCase):
    """Тесты для формы RequestContactForm"""

    def setUp(self):
        """Создание тестовых данных для формы."""

        image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=image, order_category=1
        )
        self.car = create_car('Toyota', 'Camry', 2023, 10000, self.category)

    def test_form_valid(self):
        """Тест валидной формы."""

        from contacts.forms import RequestContactForm
        from contacts.models import RequestContact
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'telephone_number': '+79000000000',
            'type_request': RequestContact.TypeRequest.CONTACT_US
        }
        form = RequestContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        """Тест формы с невалидным email."""

        from contacts.forms import RequestContactForm
        from contacts.models import RequestContact
        form_data = {
            'name': 'Test User',
            'email': 'invalid-email',
            'telephone_number': '+79000000000',
            'type_request': RequestContact.TypeRequest.CONTACT_US
        }
        form = RequestContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_empty_name(self):
        """Тест формы с пустым именем."""

        from contacts.forms import RequestContactForm
        from contacts.models import RequestContact
        form_data = {
            'name': '',
            'email': 'test@example.com',
            'telephone_number': '+79000000000',
            'type_request': RequestContact.TypeRequest.CONTACT_US
        }
        form = RequestContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_requires_car_for_autoteka(self):
        """Тест требования автомобиля для Автотеки."""

        from contacts.forms import RequestContactForm
        from contacts.models import RequestContact

        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'telephone_number': '+79000000000',
            'type_request': RequestContact.TypeRequest.AUTOTEKA,
            'car_slug': '',
        }
        form = RequestContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_form_invalid_car_slug_raises_error(self):
        """Тест невалидного slug автомобиля."""

        from contacts.forms import RequestContactForm
        from contacts.models import RequestContact

        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'telephone_number': '+79000000000',
            'type_request': RequestContact.TypeRequest.AUTOTEKA,
            'car_slug': 'unknown-slug',
        }
        form = RequestContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_form_duplicate_request_is_invalid(self):
        """Тест дубликата заявки."""

        from django.utils import timezone

        from contacts.forms import RequestContactForm
        from contacts.models import RequestContact

        existing = RequestContact.objects.create(
            name='Test User',
            email='test@example.com',
            telephone_number='+79000000000',
            type_request=RequestContact.TypeRequest.CONTACT_US,
            status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION,
        )
        existing.expires_at = timezone.now() + timedelta(hours=1)
        existing.save()

        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'telephone_number': '+79000000000',
            'type_request': RequestContact.TypeRequest.CONTACT_US,
        }
        form = RequestContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class RequestContactViewsTest(TestCase):
    """Тесты для представлений контактов"""

    def setUp(self):
        """Создание тестовых данных для представлений."""

        image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=image, order_category=1
        )
        self.car = create_car('Toyota', 'Camry', 2023, 10000, self.category)

    def test_contacts_page(self):
        """Тест доступности страницы контактов."""

        url = reverse('contacts:contacts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class ContactServiceTest(TestCase):
    """Тесты для логики ContactService"""

    def setUp(self):
        """Создание тестовых данных для ContactService."""

        from django.utils import timezone

        from contacts.models import RequestContact
        from contacts.services import ContactService

        image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=image, order_category=1
        )
        self.car = create_car('Toyota', 'Camry', 2023, 10000, self.category)
        self.service = ContactService()

        self.request_contact = RequestContact.objects.create(
            name='Test User',
            email='test@example.com',
            telephone_number='+79000000000',
            type_request=RequestContact.TypeRequest.CONTACT_US,
            status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION,
            car=None,
        )

        self.request_contact.expires_at = timezone.now() + timedelta(hours=1)
        self.request_contact.save()

    def test_check_duplicate_request_without_car(self):
        """Тест проверки дубликата заявки без автомобиля."""

        from contacts.models import RequestContact
        from contacts.services import ContactService

        has_duplicate = ContactService.check_duplicate_request(
            RequestContact.TypeRequest.CONTACT_US,
            self.request_contact.name,
            self.request_contact.email,
        )
        self.assertTrue(has_duplicate)

    def test_check_duplicate_request_with_car(self):
        """Тест проверки дубликата заявки с автомобилем."""

        from contacts.models import RequestContact
        from contacts.services import ContactService

        request_with_car = RequestContact.objects.create(
            name='Car User',
            email='car@example.com',
            telephone_number='+79000000002',
            type_request=RequestContact.TypeRequest.CONTACT_CAR,
            status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION,
            car=self.car,
        )

        has_duplicate = ContactService.check_duplicate_request(
            request_with_car.type_request,
            request_with_car.name,
            request_with_car.email,
            self.car,
        )
        self.assertTrue(has_duplicate)

    def test_check_duplicate_request_completed_ignored(self):
        """Тест игнорирования завершенных заявок при проверке дубликатов."""

        from contacts.models import RequestContact
        from contacts.services import ContactService

        self.request_contact.status = RequestContact.Status.COMPLETE
        self.request_contact.save()

        has_duplicate = ContactService.check_duplicate_request(
            self.request_contact.type_request,
            self.request_contact.name,
            self.request_contact.email,
        )
        self.assertFalse(has_duplicate)

    def test_get_car_by_slug(self):
        """Тест получения автомобиля по slug."""

        from contacts.services import ContactService

        found = ContactService.get_car_by_slug(self.car.slug)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, self.car.id)

    def test_get_car_by_slug_returns_none(self):
        """Тест возврата None при отсутствии автомобиля."""

        from contacts.services import ContactService

        found = ContactService.get_car_by_slug('non-existent-slug')
        self.assertIsNone(found)

    def test_create_request_contact(self):
        """Тест создания заявки на обратную связь."""

        from contacts.models import RequestContact
        from contacts.services import ContactService

        form_data = {
            'name': 'New User',
            'email': 'new@example.com',
            'telephone_number': '+79000000001',
            'type_request': RequestContact.TypeRequest.CONTACT_US,
            'car': None,
        }
        created = ContactService.create_request_contact(form_data)
        self.assertIsInstance(created, RequestContact)
        self.assertEqual(created.name, 'New User')

    def test_confirm_email_success(self):
        """Тест успешного подтверждения email."""

        from django.utils import timezone

        from contacts.models import RequestContact
        from contacts.services import ContactService

        self.request_contact.expires_at = timezone.now() + timedelta(hours=1)
        self.request_contact.save()

        confirmed = ContactService.confirm_email(self.request_contact.token)
        self.request_contact.refresh_from_db()

        self.assertIsInstance(confirmed, RequestContact)
        self.assertEqual(
            self.request_contact.status, RequestContact.Status.EMAIL_CONFIRMED
        )
        self.assertIsNotNone(self.request_contact.confirmed_at)

    def test_confirm_email_not_found_returns_none(self):
        """Тест возврата None при несуществующем токене."""

        from contacts.services import ContactService

        random_token = uuid.uuid4()
        self.assertIsNone(ContactService.confirm_email(random_token))

    def test_confirm_email_expired_raises(self):
        """Тест выброса исключения при истекшем токене."""

        from django.utils import timezone

        from contacts.services import ContactService

        self.request_contact.expires_at = timezone.now() - timedelta(hours=1)
        self.request_contact.save()

        with self.assertRaises(ContactService.ExpiresAtOverdue):
            ContactService.confirm_email(self.request_contact.token)

    def test_refresh_token_updates_token_and_sends_email(self):
        """Тест обновления токена и отправки email."""

        from contacts.services import ContactService
        from contacts.services.email_service import EmailContactService

        old_token = self.request_contact.token

        with patch.object(
            EmailContactService, 'send_confirmation_message'
        ) as mocked_send:
            ContactService.refresh_token(
                str(self.request_contact.token), request=None
            )
            mocked_send.assert_called_once()

        self.request_contact.refresh_from_db()
        self.assertNotEqual(old_token, self.request_contact.token)

    def test_send_autoteka_updates_status_and_complete_at(self):
        """Тест обновления статуса и даты завершения при отправке Автотеки."""

        from contacts.models import RequestContact
        from contacts.services import ContactService

        with patch(
            'contacts.services.email_service.EmailContactService.send_autoteka'
        ) as mocked_send:
            ContactService.send_autoteka(self.request_contact, request=None)
            mocked_send.assert_called_once()

        self.request_contact.refresh_from_db()
        self.assertEqual(
            self.request_contact.status, RequestContact.Status.COMPLETE
        )
        self.assertIsNotNone(self.request_contact.complete_at)
