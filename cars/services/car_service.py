from typing import TypedDict

from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404

from cars.models import Car, CarImage, CarParameter


class CarData(TypedDict):
    """Класс, описывающий возвращаемые данные из CarService"""

    car: Car
    photos: QuerySet[CarImage]


class CarService:
    """Сервис для работы с автомобилями"""

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
        from pprint import pprint
        pprint(vars(car))

        return car
