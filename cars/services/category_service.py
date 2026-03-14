from typing import TypedDict

from django.core.paginator import Page
from django.db.models import BooleanField, Case, QuerySet, Value, When

from cars.models import Car, CarCategory
from core.services import PaginationMixin


class CategoryData(TypedDict):
    """Класс, описывающий возвращаемые данные из CategoryService"""

    categories: QuerySet[CarCategory]
    page_cars: Page[Car]


class CategoryService(PaginationMixin):
    """Сервис для генерации контекста на страницу категорий"""

    NUMBER_ITEM_PAGINATION_CATEGORY = 6

    def get_context(
        self, category_slug: str, page_number: str
    ) -> CategoryData:
        """Собирает контекст для страницы категорий

        Args:
            category_slug (str): slug выбранной категории
            page_number (str): Номер страницы пагинированных автомобилей

        Returns:
            CategoryData: Словарь с категориями и пагинированными автомобилями
        """

        return {
            'categories': self._get_queryset_categories(category_slug),
            'page_cars': self.get_page_cars_in_category(
                category_slug, page_number
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
        self, category_slug: str, page_number: str
    ) -> Page[Car]:
        """Получает пагинированные автомобили из категории

        Args:
            category_slug (str): slug категории из которой нужны автомобили
            page_number (str): Номер страницы пагинированных автомобилей

        Returns:
            Page[Car]: Объект пагинированных автомобилей
        """

        queryset = self._get_queryset_cars_in_category(category_slug)
        return self.get_page_object(
            queryset, page_number, self.NUMBER_ITEM_PAGINATION_CATEGORY
        )

    @staticmethod
    def _get_queryset_cars_in_category(category_slug: str) -> QuerySet[Car]:
        """Получает QuerySet автомобилей в определенной категории

        Args:
            category_slug (str): slug категории, из которой ннужны автомобили

        Returns:
            QuerySet[Car]: QuerySet искомых автомобилей
        """

        if category_slug is None:
            return Car.objects.none()

        return Car.objects.filter(
            category__slug=category_slug
        ).prefetch_related('car_images')
