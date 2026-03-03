from typing import TypedDict

from django.core.paginator import Page
from django.db.models import Prefetch, Q, QuerySet, Value
from django.db.models.fields import CharField
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404

from cars.models import Car, CarImage, CarParameter
from core.services import PaginationMixin


class CarData(TypedDict):
    """Класс, описывающий возвращаемые данные из CarService"""

    car: Car
    photos: QuerySet[CarImage]


class CarService(PaginationMixin):
    """Сервис для работы с автомобилями"""

    NUMBER_ITEM_PAGINATION_SEARCH_CARS = 4

    def get_context(self, slug: str) -> CarData:
        """Собирает контекст для страницы автомобиля

        Args:
            slug (str): slug автомобиля, для поиска его в БД

        Returns:
            CarData: Контекст для страницы автомобиля
        """

        car = self._get_car_with_parameters(slug)

        return {
            'car': car,
            'photos': car.car_images.all()
        }

    def _get_car_with_parameters(self, slug: str) -> Car:
        """Достает автомобиль из БД и присоединяет к модели его параметры

        Args:
            slug (str): slug искомой модели автомобиля

        Returns:
            Car: Объект модели автомобиля с параметрами
        """

        prefetches = [
            Prefetch(
                'parameters',
                queryset=CarParameter.objects.filter(
                    type_parameter=param_key
                ).order_by('key'), to_attr=f'{param_key}_parameters'
            ) for param_key, _ in CarParameter.TypeParameter.choices
        ]
        car = get_object_or_404(
            Car.objects.prefetch_related('car_images', *prefetches),
            slug=slug
        )

        return car

    def get_search_cars_page(
        self, search: str, page_number: str
    ) -> Page[Car]:
        """Собирает пагинированные данные по поиску автомобилей

        Args:
            search (str): Строка поиска
            page_number (str): Номер страницы

        Returns:
            Page[Car]: Пагинированные данные
        """

        search_field = Concat(
            'brand', Value(' '), 'model', Value(' '), 'year_release',
            output_field=CharField()
        )

        queryset = Car.objects.annotate(search_text=search_field).filter(
            Q(search_text__icontains=search) |
            Q(brand__icontains=search) |
            Q(model__icontains=search) |
            Q(year_release__icontains=search)
        )

        return self.get_page_object(
            queryset, page_number, self.NUMBER_ITEM_PAGINATION_SEARCH_CARS
        )
