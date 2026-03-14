from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from cars.models import Car, CarCategory
from core.services import PaginationMixin
from core.context_processors import current_year
from homepage.models import Feedback, HomepageImage
from homepage.services.index_service import IndexService


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
class FeedbackModelTest(TestCase):
    """Тесты для модели Feedback"""

    def setUp(self):
        """Создание тестовых данных для Feedback модели."""

        self.feedback = Feedback.objects.create(
            feedback_avito_id=12345,
            name_user='Test User',
            feedback='Great service!',
            score=5,
            date_create=date.today()
        )

    def test_feedback_creation(self):
        """Тест создания отзыва."""

        self.assertEqual(self.feedback.name_user, 'Test User')
        self.assertEqual(self.feedback.score, 5)

    def test_feedback_ordering(self):
        """Тест сортировки отзывов по ID (от новых к старым)."""

        Feedback.objects.create(
            feedback_avito_id=12346,
            name_user='User 2',
            feedback='Another',
            date_create=date(2023, 1, 1)
        )
        feedbacks = list(Feedback.objects.all())
        self.assertEqual(feedbacks[0].feedback_avito_id, 12346)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class HomepageImageModelTest(TestCase):
    """Тесты для модели HomepageImage"""

    def setUp(self):
        """Создание тестовых данных для HomepageImage."""

        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.homepage_image = HomepageImage.objects.create(
            image=self.image, caption='Test', order_image=1
        )

    def test_homepage_image_creation(self):
        """Тест создания изображения для главной страницы."""

        self.assertEqual(self.homepage_image.caption, 'Test')


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class HomepageViewsTest(TestCase):
    """Тесты для представлений главной страницы"""

    def setUp(self):
        """Создание тестовых данных для представлений."""

        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=self.image, order_category=1
        )
        self.car = create_car(
            'Toyota', 'Camry', 2023, 10000, self.category,
            price=3000000, is_special_offer=True
        )
        self.feedback = Feedback.objects.create(
            feedback_avito_id=12345,
            name_user='Test User',
            feedback='Great!',
            score=5,
            date_create=date.today()
        )

    def test_index_view(self):
        """Тест доступности главной страницы."""

        url = reverse('homepage:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_context_data(self):
        """Тест контекстных данных главной страницы."""

        url = reverse('homepage:index')
        response = self.client.get(url)
        self.assertIn('page_special_offers', response.context)
        self.assertIn('page_feedbacks', response.context)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class PaginationMixinTest(TestCase):
    """Тесты для утилиты пагинации"""

    def setUp(self):
        """Создание тестовых данных для пагинации."""

        class DummyPagination(PaginationMixin):
            pass

        self.mixin = DummyPagination()
        self.items = list(range(10))

    def test_get_page_object_returns_page(self):
        """Тест получения страницы объектов."""

        page = self.mixin.get_page_object(
            self.items, page_number=1, per_page=3
        )
        self.assertEqual(len(page.object_list), 3)

    def test_get_page_object_returns_page_data_dict(self):
        """Тест получения данных страницы в виде словаря."""

        page_data = self.mixin.get_page_object(
            self.items, page_number=1, per_page=3, is_object=False
        )
        self.assertIn('page', page_data)
        self.assertIn('has_pages', page_data)
        self.assertIn('has_next', page_data['has_pages'])
        self.assertIn('has_previous', page_data['has_pages'])

    def test_get_page_object_handles_invalid_and_empty_page(self):
        """Тест обработки некорректных и пустых страниц."""

        page_invalid = self.mixin.get_page_object(
            self.items, page_number='invalid', per_page=3
        )
        self.assertEqual(page_invalid.number, 1)

        page_too_big = self.mixin.get_page_object(
            self.items, page_number=999, per_page=3
        )
        self.assertEqual(page_too_big.number, page_too_big.paginator.num_pages)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class IndexServiceTest(TestCase):
    """Тесты для логики IndexService"""

    def setUp(self):
        """Создание тестовых данных для IndexService."""

        self.factory = RequestFactory()
        self.service = IndexService()

        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=self.image, order_category=1
        )

        self.special_car = create_car(
            'Toyota', 'Camry', 2023, 10000, self.category,
            price=3000000, is_special_offer=True, sold=False
        )
        self.sold_special = create_car(
            'Honda', 'Civic', 2022, 20000, self.category,
            price=2000000, is_special_offer=True, sold=True
        )

        self.feedback_1 = Feedback.objects.create(
            feedback_avito_id=1,
            name_user='User 1',
            feedback='Good',
            score=5,
            date_create=date(2023, 1, 1),
        )
        self.feedback_2 = Feedback.objects.create(
            feedback_avito_id=2,
            name_user='User 2',
            feedback='Ok',
            score=3,
            date_create=date(2023, 1, 2),
        )

        self.homepage_image = HomepageImage.objects.create(
            image=self.image, caption='Test', order_image=1
        )

    def test_get_index_context_structure(self):
        """Тест структуры контекста главной страницы."""

        request = self.factory.get('/')
        context = self.service.get_index_context(request)

        self.assertIn('dealership_images', context)
        self.assertIn('page_special_offers', context)
        self.assertIn('page_feedbacks', context)
        self.assertIn('feedbacks_stats', context)

    def test_get_page_special_offers_returns_only_active_offers(self):
        """Тест получения только активных спецпредложений."""

        request = self.factory.get('/', {'special_offers_page': 1})
        page = self.service.get_page_special_offers(request)

        self.assertIn(self.special_car, page.object_list)
        self.assertNotIn(self.sold_special, page.object_list)

    def test_get_page_special_offers_page_data_variant(self):
        """Тест получения данных страницы спецпредложений."""

        request = self.factory.get('/', {'special_offers_page': 1})
        page_data = self.service.get_page_special_offers(
            request, is_object=False
        )

        self.assertIn('page', page_data)
        self.assertIn('has_pages', page_data)

    def test_get_page_feedbacks_returns_page_and_data(self):
        """Тест получения страницы отзывов."""

        request = self.factory.get('/', {'feedbacks_page': 1})

        page = self.service.get_page_feedbacks(request)
        self.assertIn(self.feedback_1, page.object_list)

        page_data = self.service.get_page_feedbacks(request, is_object=False)
        self.assertIn('page', page_data)
        self.assertIn('has_pages', page_data)

    def test_get_feedbacks_stats_returns_avg_and_count(self):
        """Тест получения статистики отзывов."""

        stats = self.service._get_feedbacks_stats()
        self.assertEqual(stats['feedbacks_count'], 2)
        self.assertAlmostEqual(stats['avg_score'], 4.0)

    def test_current_year_context_processor(self):
        """Тест контекстного процессора текущего года."""

        context = current_year(request=None)
        self.assertIn('now', context)
