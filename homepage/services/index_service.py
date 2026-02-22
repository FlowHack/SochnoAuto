from typing import Any, overload

from django.core.paginator import Page
from django.db.models import Avg, Count, Prefetch, QuerySet
from django.http import HttpRequest

from cars.models import Car, CarImage
from core.services import PaginationMixin, PageData
from homepage.models import Feedback, HomepageImage


class IndexService(PaginationMixin):
    """Сервис для главной страницы"""

    NUMBER_ITEM_PAGINATOR_FEEDBACKS = 3
    NUMBER_ITEM_PAGINATOR_SPECIAL_OFFERS = 3

    def get_index_context(self, request: HttpRequest) -> dict[str, Any]:
        """Получает контекст для главной страницы

        Args:
            request: Объект запроса с информацией

        Return: Словарь с данными для контекста страницы
        """

        return {
            'dealership_images': self._get_dealership_images(),
            'page_special_offers': self.get_page_special_offers(request),
            'page_feedbacks': self.get_page_feedbacks(request),
            'feedbacks_stats': self._get_feedbacks_stats()
        }

    def _get_dealership_images(self) -> list[HomepageImage]:
        """Получает список картинок для превью на главной странице"""

        return HomepageImage.objects.all()

    @overload
    def get_page_special_offers(
        self, request: HttpRequest, is_object: bool = False
    ) -> PageData: ...

    @overload
    def get_page_special_offers(
        self, request: HttpRequest, is_object: bool = True
    ) -> Page[Car]: ...

    def get_page_special_offers(
        self, request: HttpRequest, is_object: bool = True
    ) -> Page[Car] | PageData:
        """Функция для для получения пагинированных специальных предложений

        Args:
            request: Объект запроса
            is_object: Необходимо вернуть только объект пагинации или еще и
                дополнительную информацию о наличии страниц

        Return: Объект пагинации или словарь с информацией о пагинации
            вместе с объектом
        """

        page_number = request.GET.get('special_offers_page')
        queryset = self._get_queryset_special_offers()
        return self.get_page_object(
            queryset, page_number, self.NUMBER_ITEM_PAGINATOR_SPECIAL_OFFERS,
            is_object
        )

    def _get_queryset_special_offers(self) -> QuerySet[Car]:
        """Получает QuerySet для специальных предложений на
        главную страницу
        """

        return Car.objects.filter(
            is_special_offer=True, sold=False
        ).order_by('date_is_special_offer').prefetch_related(
            Prefetch(
                'car_images',
                CarImage.objects.order_by('order_image'),
                to_attr='ordered_images'
            )
        )

    @overload
    def get_page_feedbacks(
        self, request: HttpRequest, is_object: bool = False
    ) -> PageData: ...

    @overload
    def get_page_feedbacks(
        self, request: HttpRequest, is_object: bool = True
    ) -> Page[Feedback]: ...

    def get_page_feedbacks(
        self, request: HttpRequest, is_object: bool = True
    ) -> Page[Feedback] | PageData:
        """Функция для получения пагинированных отзывов

        Args:
            request: Объект запроса
            is_object: Необходимо вернуть только объект пагинации или еще и
                дополнительную информацию о наличии страниц

        Return: Объект пагинации или словарь с информацией о пагинации
            вместе с объектом
        """

        page_number = request.GET.get('feedbacks_page')
        queryset = self._get_queryset_feedbacks()
        return self.get_page_object(
            queryset, page_number, self.NUMBER_ITEM_PAGINATOR_FEEDBACKS,
            is_object
        )

    def _get_queryset_feedbacks(self) -> QuerySet[Feedback]:
        """Получает список отзывов"""

        return Feedback.objects.all().order_by('date_create')

    def _get_feedbacks_stats(self) -> dict[str, Any]:
        """Получает количество и среднее значение отзывов"""

        stats = Feedback.objects.aggregate(
            avg_score=Avg('score'), count_feedbacks=Count('id')
        )
        return {
            'avg_score': (
                round(stats['avg_score'], 1)
                if stats['avg_score'] is not None
                else None
            ),
            'feedbacks_count': stats['count_feedbacks']
        }
