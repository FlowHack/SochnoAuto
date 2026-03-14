from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from cars.models import Car, CarCategory
from homepage.models import Feedback


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
class SpecialOffersAPITest(TestCase):
    """Тесты для API спецпредложений"""

    def setUp(self):
        """Создание тестовых данных для API спецпредложений."""

        image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=image, order_category=1
        )
        create_car(
            'Toyota', 'Camry', 2023, 10000, self.category,
            price=3000000, is_special_offer=True
        )
        create_car(
            'Honda', 'Civic', 2022, 20000, self.category,
            price=2500000, is_special_offer=False
        )

    def test_special_offers_api_get(self):
        """Тест получения списка спецпредложений."""

        url = reverse('api:special_offers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class FeedbacksAPITest(TestCase):
    """Тесты для API отзывов"""

    def setUp(self):
        """Создание тестовых данных для API отзывов."""

        from datetime import date
        self.feedback = Feedback.objects.create(
            feedback_avito_id=12345,
            name_user='Test User',
            feedback='Great!',
            score=5,
            date_create=date.today()
        )

    def test_feedbacks_api_get(self):
        """Тест получения списка отзывов."""

        url = reverse('api:feedbacks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class CategoryAPITest(TestCase):
    """Тесты для API категорий"""

    def setUp(self):
        """Создание тестовых данных для API категорий."""

        image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=image, order_category=1
        )
        create_car(
            'Toyota', 'Camry', 2023, 10000, self.category,
            price=3000000
        )

    def test_category_api_get(self):
        """Тест получения автомобилей по категории."""

        url = (
            reverse('api:category') +
            f'?category={self.category.slug}&page=1'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_api_missing_params(self):
        """Тест API категории без параметров."""

        url = reverse('api:category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class SearchCarAPITest(TestCase):
    """Тесты для API поиска автомобилей"""

    def setUp(self):
        """Создание тестовых данных для API поиска."""

        image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=image, order_category=1
        )
        create_car(
            'Toyota', 'Camry', 2023, 10000, self.category, price=3000000
        )

    def test_search_car_api_get(self):
        """Тест поиска автомобилей."""

        url = reverse('api:search_car') + '?search=Toyota'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
