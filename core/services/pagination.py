from typing import Sequence, TypedDict, TypeVar, overload

from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.db.models import QuerySet
from rest_framework.utils.serializer_helpers import ReturnList

T = TypeVar('T')


class PageData(TypedDict):
    class HasPagesData(TypedDict):
        has_next: bool
        has_previous: bool

    page: Page[T]
    has_pages: HasPagesData


class PaginationMixin:
    """Универсальная пагинация для всех сервисов"""

    @overload
    def get_page_object(
        self,
        queryset: QuerySet[T] | list[T] | ReturnList[T] | Sequence[T],
        page_number: str | int | None,
        per_page: int,
        is_object: bool = True,
    ) -> Page[T]: ...

    @overload
    def get_page_object(
        self,
        queryset: QuerySet[T] | list[T] | ReturnList[T] | Sequence[T],
        page_number: str | int | None,
        per_page: int,
        is_object: bool = False,
    ) -> PageData: ...

    def get_page_object(
        self,
        queryset: QuerySet[T] | list[T] | ReturnList[T] | Sequence[T],
        page_number: str | int | None,
        per_page: int,
        is_object: bool = True
    ) -> Page[T] | PageData:
        """Создает пагинацию по данным

        Args:
            queryset: Принимает Django QuerySet, список,
                Serializer.data или иной итерируемый объект
            page_number: Номер страницы, может быть строкой, числом или None
            per_page: Сколько элементов должно быть на странице
            is_object: Ожидается получить объект пагинатора или основные
                значения

        Return: Объект пагинатора или словарь со значениями объекта
        """

        paginator = Paginator(queryset, per_page)
        page: Page[T]
        try:
            page = paginator.get_page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        if is_object:
            return page
        return self._get_all_values_from_page(page)

    @staticmethod
    def _get_all_values_from_page(page: Page[T]) -> PageData:
        """Приватный метод для получения словаря со значениями объекта Page

        Args:
            page: Объект Page пагинатора

        Return: Словарь со значениями есть ли страница до и после и object_list
        """
        return {
            'page': {
                'object_list': page.object_list,
                'number': page.number,
                'num_pages': page.paginator.num_pages
            },
            'has_pages': {
                'has_next': page.has_next(),
                'has_previous': page.has_previous()
            }
        }
