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
        self.special_car = create_car(
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

    def test_special_offers_returns_json_structure(self):
        """Тест структуры JSON ответа."""

        url = reverse('api:special_offers')
        response = self.client.get(url)
        data = response.json()
        self.assertIn('page', data)
        self.assertIn('has_pages', data)
        self.assertIn('object_list', data['page'])
        self.assertIsInstance(data['page']['object_list'], list)

    def test_special_offers_only_special_offers(self):
        """Тест что возвращаются только спецпредложения."""

        url = reverse('api:special_offers')
        response = self.client.get(url)
        data = response.json()
        cars = data['page']['object_list']
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0]['brand'], 'Toyota')

    def test_special_offers_pagination(self):
        """Тест пагинации спецпредложений."""

        for i in range(5):
            create_car(
                f'Brand{i}', f'Model{i}', 2023, 10000, self.category,
                price=3000000, is_special_offer=True
            )
        url = reverse('api:special_offers') + '?special_offers_page=1'
        response = self.client.get(url)
        data = response.json()
        self.assertIn('num_pages', data['page'])
        self.assertIn('number', data['page'])
        self.assertIn('has_next', data['has_pages'])
        self.assertIn('has_previous', data['has_pages'])

    def test_special_offers_returns_empty_when_no_offers(self):
        """Тест пустого списка при отсутствии спецпредложений."""

        from cars.models import Car
        Car.objects.filter(is_special_offer=True).delete()
        url = reverse('api:special_offers')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(len(data['page']['object_list']), 0)


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

    def test_feedbacks_returns_json_structure(self):
        """Тест структуры JSON ответа."""

        url = reverse('api:feedbacks')
        response = self.client.get(url)
        data = response.json()
        self.assertIn('page', data)
        self.assertIn('has_pages', data)
        self.assertIn('object_list', data['page'])

    def test_feedbacks_data_fields(self):
        """Тест полей данных отзыва."""

        url = reverse('api:feedbacks')
        response = self.client.get(url)
        data = response.json()
        feedbacks = data['page']['object_list']
        self.assertEqual(len(feedbacks), 1)
        feedback = feedbacks[0]
        self.assertEqual(feedback['name_user'], 'Test User')
        self.assertEqual(feedback['feedback'], 'Great!')
        self.assertEqual(feedback['score'], 5)
        self.assertIn('avatar_url', feedback)

    def test_feedbacks_without_avatar(self):
        """Тест отзыва без аватара."""

        from datetime import date
        Feedback.objects.create(
            feedback_avito_id=54321,
            name_user='No Avatar User',
            feedback='No avatar!',
            score=3,
            date_create=date.today()
        )
        url = reverse('api:feedbacks')
        response = self.client.get(url)
        data = response.json()
        feedbacks = data['page']['object_list']
        avatar_urls = [f.get('avatar_url') for f in feedbacks]
        self.assertTrue(any(url is None for url in avatar_urls))

    def test_feedbacks_returns_empty_when_no_feedbacks(self):
        """Тест пустого списка при отсутствии отзывов."""

        Feedback.objects.all().delete()
        url = reverse('api:feedbacks')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(len(data['page']['object_list']), 0)

    def test_feedbacks_pagination(self):
        """Тест пагинации отзывов."""

        from datetime import date
        for i in range(10):
            Feedback.objects.create(
                feedback_avito_id=1000 + i,
                name_user=f'User{i}',
                feedback=f'Feedback {i}',
                score=5,
                date_create=date.today()
            )
        url = reverse('api:feedbacks') + '?feedbacks_page=1'
        response = self.client.get(url)
        data = response.json()
        self.assertIn('num_pages', data['page'])
        self.assertIn('number', data['page'])


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
        self.car = create_car(
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

    def test_category_returns_json_structure(self):
        """Тест структуры JSON ответа."""

        url = (
            reverse('api:category') +
            f'?category={self.category.slug}&page=1'
        )
        response = self.client.get(url)
        data = response.json()
        self.assertIn('page', data)
        self.assertIn('has_pages', data)
        self.assertIn('object_list', data['page'])

    def test_category_only_returns_cars_from_category(self):
        """Тест что возвращаются только автомобили из категории."""

        image = SimpleUploadedFile(
            'test2.jpg', b'file_content', content_type='image/jpeg'
        )
        other_category = CarCategory.objects.create(
            name='Грузовые', image=image, order_category=2
        )
        create_car(
            'MAN', 'Truck', 2020, 50000, other_category,
            price=5000000
        )
        url = (
            reverse('api:category') +
            f'?category={self.category.slug}&page=1'
        )
        response = self.client.get(url)
        data = response.json()
        cars = data['page']['object_list']
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0]['brand'], 'Toyota')

    def test_category_returns_empty_when_no_cars_in_category(self):
        """Тест пустого списка при отсутствии автомобилей в категории."""

        from cars.models import Car
        Car.objects.filter(category=self.category).delete()
        url = reverse('api:category') + f'?category={self.category.slug}&page=1'
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(len(data['page']['object_list']), 0)


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
        self.toyota = create_car(
            'Toyota', 'Camry', 2023, 10000, self.category, price=3000000
        )
        self.honda = create_car(
            'Honda', 'Civic', 2022, 20000, self.category, price=2500000
        )

    def test_search_car_api_get(self):
        """Тест поиска автомобилей."""

        url = reverse('api:search_car') + '?search=Toyota'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_car_returns_json_structure(self):
        """Тест структуры JSON ответа."""

        url = reverse('api:search_car') + '?search=Toyota'
        response = self.client.get(url)
        data = response.json()
        self.assertIn('page', data)
        self.assertIn('has_pages', data)
        self.assertIn('object_list', data['page'])

    def test_search_finds_by_brand(self):
        """Тест поиска по марке."""

        url = reverse('api:search_car') + '?search=Toyota'
        response = self.client.get(url)
        data = response.json()
        cars = data['page']['object_list']
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0]['brand'], 'Toyota')

    def test_search_finds_by_model(self):
        """Тест поиска по модели."""

        url = reverse('api:search_car') + '?search=Camry'
        response = self.client.get(url)
        data = response.json()
        cars = data['page']['object_list']
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0]['model'], 'Camry')

    def test_search_returns_empty_for_no_match(self):
        """Тест пустого результата при отсутствии совпадений."""

        url = reverse('api:search_car') + '?search=BMW'
        response = self.client.get(url)
        data = response.json()
        cars = data['page']['object_list']
        self.assertEqual(len(cars), 0)

    def test_search_requires_query(self):
        """Тест что поиск требует параметр search."""

        url = reverse('api:search_car')
        response = self.client.get(url)
        data = response.json()
        cars = data['page']['object_list']
        self.assertEqual(len(cars), 0)
