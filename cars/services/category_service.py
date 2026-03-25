from typing import TypedDict

from django.core.paginator import Page
from django.db.models import BooleanField, Case, QuerySet, Value, When
from django.http import HttpRequest
from rest_framework.utils.serializer_helpers import ReturnList

from api.serializers import CarWithImagesSerializer
from cars.models import Car, CarCategory
from core.services import PageData, PaginationMixin


class CategoryData(TypedDict):
    """Класс, описывающий возвращаемые данные из CategoryService"""

    categories: QuerySet[CarCategory]
    page_cars: Page[Car]


class CategoryService(PaginationMixin):
    """Сервис для генерации контекста на страницу категорий"""

    NUMBER_ITEM_PAGINATION_CATEGORY = 6

    def get_context(
        self, request: HttpRequest
    ) -> CategoryData:
        """Собирает контекст для страницы категорий

        Args:
            request (HttpRequest): Объект запроса

        Returns:
            CategoryData: Словарь с категориями и пагинированными автомобилями
        """
        category_slug = request.GET.get('category')

        return {
            'categories': self._get_queryset_categories(category_slug),
            'page_cars': self.get_page_cars_in_category(
                request, category_slug, is_object=True
            ),
            'selected_category': category_slug
        }

    @staticmethod
    def _get_queryset_categories(category_slug: str) -> QuerySet[CarCategory]:
        """Получает QuerySet для категорий

        Args:
            category_slug (str): Какую категорию выбрали

        Returns:
            QuerySet[CarCategory]: QuerySet с категориями
        """

        return CarCategory.objects.annotate(
            selected_category=Case(
                When(slug=category_slug, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

    def get_page_cars_in_category(
        self, request: HttpRequest, category_slug: str = None,
        is_object: bool = True
    ) -> Page[Car] | PageData:
        """Получает пагинированные автомобили из категории

        Args:
            request (HttpRequest): Объект запроса
            category_slug (str): slug категории, из которой нужны автомобили.
                Defaults to None.
            is_object (bool, optional): Указывает, нужно ли вернуть объект
                пагинации или словарь с информацией о пагинации.
                Defaults to True.

        Returns:
            Page[Car] | PageData: Объект пагинированных автомобилей или
                словарь с информацией о пагинации вместе с пагинированными
                данными
        """
        category_slug = category_slug or request.GET.get('category')
        page_number = request.GET.get('page')

        queryset = self._get_queryset_cars_in_category(
            category_slug, is_object
        )
        return self.get_page_object(
            queryset, page_number, self.NUMBER_ITEM_PAGINATION_CATEGORY,
            is_object
        )

    @staticmethod
    def _get_queryset_cars_in_category(
        category_slug: str, is_object: bool
    ) -> QuerySet[Car] | ReturnList[CarWithImagesSerializer]:
        """Получает QuerySet автомобилей в определенной категории

        Args:
            category_slug (str): slug категории, из которой ннужны автомобили
            is_object (bool): Указывает, нужно ли вернуть QuerySet или словарь
                с информацией о пагинации

        Returns:
            QuerySet[Car]: QuerySet искомых автомобилей или сериализованные
                данные автомобилей в категории
        """

        if category_slug is None:
            return Car.objects.none()

        queryset = Car.objects.filter(
            category__slug=category_slug
        ).order_by('-pub_date').prefetch_related('car_images')

        if is_object:
            return queryset
        return CarWithImagesSerializer(queryset, many=True).data
