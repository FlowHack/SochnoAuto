from typing import TypedDict

from django.db.models import Prefetch, Q, QuerySet, Value
from django.db.models.fields import CharField
from django.db.models.functions import Concat
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ReturnList

from api.serializers import CarWithImagesSerializer
from cars.models import Car, CarImage, CarParameter
from core.services import PaginationMixin


class CarData(TypedDict):
    """Класс, описывающий возвращаемые данные из CarService"""

    car: Car
    photos: QuerySet[CarImage]


class CarService(PaginationMixin):
    """Сервис для работы с автомобилями"""

    NUMBER_ITEM_PAGINATION_SEARCH_CARS = 3

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
        return get_object_or_404(
            Car.objects.prefetch_related('car_images', *prefetches),
            slug=slug
        )

    def get_search_cars_page(
        self, request: HttpRequest
    ) -> ReturnList[Car]:
        """Собирает пагинированные данные по поиску автомобилей

        Args:
            request (HttpRequest): Объект запроса, из которого извлекаются
                данные для поиска и пагинации

        Returns:
            Page[Car]: Пагинированные данные
        """

        search_query = request.GET.get('search')
        page_number = request.GET.get('page')

        queryset = self._get_queryset_search_cars(search_query)

        serialized_data = CarWithImagesSerializer(queryset, many=True).data

        return self.get_page_object(
            serialized_data, page_number,
            self.NUMBER_ITEM_PAGINATION_SEARCH_CARS,  False
        )

    def _get_queryset_search_cars(self, search_query: str) -> QuerySet[Car]:
        """Собирает QuerySet по поиску автомобилей

        Args:
            search_query (str): Строка для поиска

        Returns:
            QuerySet[Car]: QuerySet с результатами поиска
        """

        if not search_query:
            return Car.objects.none()

        search_field = Concat(
            'brand', Value(' '), 'model', Value(' '), 'year_release',
            output_field=CharField()
        )

        return Car.objects.annotate(search_text=search_field).filter(
            Q(search_text__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(year_release__icontains=search_query)
        ).order_by('-year_release').prefetch_related('car_images')
