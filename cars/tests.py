from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Page
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.utils.text import slugify

from cars.models import Car, CarCategory, CarImage, CarParameter
from cars.services.car_service import CarService
from cars.services.category_service import CategoryService


def create_car(brand, model, year_release, mileage, category, **kwargs):
    """Вспомогательная функция для создания автомобиля в тестах."""

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
class CarCategoryModelTest(TestCase):
    """Тесты для модели CarCategory"""

    def setUp(self):
        """Создание тестовых данных для категории автомобилей."""

        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=self.image, order_category=1
        )

    def test_category_creation(self):
        """Тест создания категории."""

        self.assertEqual(self.category.name, 'Легковые')
        self.assertEqual(self.category.order_category, 1)

    def test_category_slug_generation(self):
        """Тест генерации слага для категории."""

        self.assertEqual(self.category.slug, 'легковые')

    def test_category_ordering(self):
        """Тест сортировки категорий."""

        CarCategory.objects.create(
            name='Грузовые', image=self.image, order_category=0
        )
        categories = list(CarCategory.objects.all())
        self.assertEqual(categories[0].name, 'Грузовые')


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class CarModelTest(TestCase):
    """Тесты для модели Car"""

    def setUp(self):
        """Создание тестовых данных для автомобиля."""

        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=self.image, order_category=1
        )
        self.car = create_car(
            'Toyota', 'Camry', 2023, 10000, self.category,
            fuel_type=Car.FuelTypes.GASOLINE,
            wheel_position=Car.WheelPosition.LEFT,
            type_transmission=Car.TypeTransmission.AT,
            car_body=Car.CarBody.SEDAN,
            price=3000000
        )

    def test_car_creation(self):
        """Тест создания автомобиля."""

        self.assertEqual(self.car.brand, 'Toyota')
        self.assertEqual(self.car.model, 'Camry')
        self.assertEqual(self.car.year_release, 2023)
        self.assertEqual(self.car.price, 3000000)

    def test_car_full_name_property(self):
        """Тест свойства полного имени автомобиля."""

        self.assertEqual(self.car.full_name, 'Toyota Camry 2023')

    def test_car_special_offer_sets_date(self):
        """Тест установки даты при активации спецпредложения."""

        self.assertIsNone(self.car.date_is_special_offer)
        self.car.is_special_offer = True
        self.car.save()
        self.assertIsNotNone(self.car.date_is_special_offer)

    def test_car_sold_clears_special_offer(self):
        """Тест сброса спецпредложения при продаже."""

        self.car.is_special_offer = True
        self.car.save()
        self.car.sold = True
        self.car.save()
        self.car.refresh_from_db()
        self.assertFalse(self.car.is_special_offer)

    def test_car_fuel_types_choices(self):
        """Тест выбора типов топлива."""

        self.assertIn(('gasoline', 'Бензин'), Car.FuelTypes.choices)
        self.assertIn(('diesel', 'Дизель'), Car.FuelTypes.choices)

    def test_car_transmission_choices(self):
        """Тест выбора типов трансмиссии."""

        self.assertIn(('at', 'Автомат'), Car.TypeTransmission.choices)
        self.assertIn(('mt', 'Механика'), Car.TypeTransmission.choices)

    def test_car_body_choices(self):
        """Тест выбора типов кузова."""

        self.assertIn(('sedan', 'Седан'), Car.CarBody.choices)
        self.assertIn(('suv', 'Внедорожник'), Car.CarBody.choices)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class CarImageModelTest(TestCase):
    """Тесты для модели CarImage"""

    def setUp(self):
        """Создание тестовых данных для изображения автомобиля."""

        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=self.image, order_category=1
        )
        self.car = create_car('Toyota', 'Camry', 2023, 10000, self.category)
        self.car_image = CarImage.objects.create(
            car=self.car, image=self.image, caption='Test', order_image=1
        )

    def test_car_image_creation(self):
        """Тест создания изображения автомобиля."""

        self.assertEqual(self.car_image.car, self.car)
        self.assertEqual(self.car_image.caption, 'Test')


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class CarParameterModelTest(TestCase):
    """Тесты для модели CarParameter"""

    def setUp(self):
        """Создание тестовых данных для параметра автомобиля."""

        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=self.image, order_category=1
        )
        self.car = create_car('Toyota', 'Camry', 2023, 10000, self.category)
        self.parameter = CarParameter.objects.create(
            car=self.car, type_parameter=CarParameter.TypeParameter.COMFORT,
            key='Кондиционер', value='Автоматический', uom='шт.')

    def test_parameter_creation(self):
        """Тест создания параметра автомобиля."""

        self.assertEqual(self.parameter.key, 'Кондиционер')
        self.assertEqual(self.parameter.value, 'Автоматический')

    def test_parameter_type_choices(self):
        """Тест выбора типов параметров."""

        self.assertIn(
            ('comfort', 'Комфорт'), CarParameter.TypeParameter.choices
        )
        self.assertIn(
            ('technical', 'Технический'), CarParameter.TypeParameter.choices
        )


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class CarViewsTest(TestCase):
    """Тесты для представлений автомобилей"""

    def setUp(self):
        """Создание тестовых данных для представлений."""

        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=self.image, order_category=1
        )
        self.car = create_car(
            'Toyota', 'Camry', 2023, 10000, self.category, price=3000000
        )

    def test_category_view(self):
        """Тест представления категории автомобилей."""

        url = reverse('cars:category') + f'?category={self.category.slug}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_car_detail_view(self):
        """Тест детального представления автомобиля."""

        url = reverse('cars:car', args=[self.car.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class CarModelValidationTest(TestCase):
    """Тесты для валидации модели Car"""

    def setUp(self):
        """Создание тестовых данных для валидации."""

        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=self.image, order_category=1
        )

    def test_invalid_year_too_old(self):
        """Тест слишком старого года выпуска."""

        with self.assertRaises(Exception):
            Car.objects.create(
                brand='Toyota', model='Camry', year_release=1800,
                mileage=10000, category=self.category
            )

    def test_invalid_year_future(self):
        """Тест будущего года выпуска."""

        future_year = date.today().year + 2
        with self.assertRaises(Exception):
            Car.objects.create(
                brand='Toyota', model='Camry', year_release=future_year,
                mileage=10000, category=self.category
            )

    def test_negative_mileage(self):
        """Тест отрицательного пробега."""

        with self.assertRaises(Exception):
            Car.objects.create(
                brand='Toyota', model='Camry', year_release=2023,
                mileage=-1000, category=self.category
            )


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class CarServiceTest(TestCase):
    """Тесты для логики CarService"""

    def setUp(self):
        """Создание тестовых данных для CarService."""

        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category = CarCategory.objects.create(
            name='Легковые', image=self.image, order_category=1
        )
        self.car = create_car('Toyota', 'Camry', 2023, 10000, self.category)
        self.photo = CarImage.objects.create(
            car=self.car, image=self.image, caption='Front', order_image=1
        )
        self.service = CarService()

    def test_get_context_returns_car_and_photos(self):
        """Тест получения контекста автомобиля с фотографиями."""

        context = self.service.get_context(self.car.slug)
        self.assertIn('car', context)
        self.assertIn('photos', context)
        self.assertEqual(context['car'], self.car)
        self.assertIn(self.photo, list(context['photos']))

    def test_get_search_cars_page_returns_page_and_filters(self):
        """Тест получения страницы поиска автомобилей."""

        from django.test import RequestFactory
        create_car('Toyota', 'Corolla', 2020, 20000, self.category)
        create_car('Honda', 'Civic', 2020, 15000, self.category)

        factory = RequestFactory()
        request = factory.get('/', {'search': 'Toyota', 'page': '1'})
        page_data = self.service.get_search_cars_page(request)
        self.assertIn('page', page_data)
        self.assertIn('has_pages', page_data)
        self.assertIsInstance(page_data['page']['object_list'], list)


@override_settings(DEFAULT_AUTO_FIELD='django.db.models.BigAutoField')
class CategoryServiceTest(TestCase):
    """Тесты для логики CategoryService"""

    def setUp(self):
        """Создание тестовых данных для CategoryService."""

        self.factory = RequestFactory()
        self.image = SimpleUploadedFile(
            'test.jpg', b'file_content', content_type='image/jpeg'
        )
        self.category1 = CarCategory.objects.create(
            name='Легковые', image=self.image, order_category=1
        )
        self.category2 = CarCategory.objects.create(
            name='Грузовые', image=self.image, order_category=2
        )
        self.car1 = create_car('Toyota', 'Camry', 2023, 10000, self.category1)
        self.car2 = create_car('MAN', 'Truck', 2020, 50000, self.category2)
        self.service = CategoryService()

    def test_get_context_returns_selected_category_and_page_cars(self):
        """Тест получения контекста с выбранной категорией."""

        request = self.factory.get('/', {
            'category': self.category1.slug,
            'page': '1'
        })
        context = self.service.get_context(request)

        self.assertIn('categories', context)
        self.assertIn('page_cars', context)
        self.assertEqual(context['selected_category'], self.category1.slug)

        categories = context['categories']
        selected = categories.get(slug=self.category1.slug)
        other = categories.get(slug=self.category2.slug)

        self.assertTrue(selected.selected_category)
        self.assertFalse(other.selected_category)
        self.assertIn(self.car1, list(context['page_cars'].object_list))

    def test_get_queryset_cars_in_category_none_returns_empty(self):
        """Тест получения пустого QuerySet при отсутствии категории."""

        empty_qs = CategoryService._get_queryset_cars_in_category(None, is_object=True)
        self.assertEqual(empty_qs.count(), 0)
