from typing import Any

from django.core.paginator import Page
from django.db.models import Avg, Count, Prefetch, QuerySet
from django.http import HttpRequest

from cars.models import Car, CarImage
from core.services import PaginationMixin
from homepage.models import Feedback, HomepageImage


class IndexService(PaginationMixin):
    """Сервис для главной страницы"""

    NUMBER_ITEM_PAGINATOR_FEEDBACKS = 6
    NUMBER_ITEM_PAGINATOR_SPECIAL_OFFERS = 3

    def get_index_context(self, request: HttpRequest) -> dict[str, Any]:
        """Получает контекст для главной страницы"""

        return {
            'dealership_images': self._get_dealership_images(),
            'page_special_offers': self._get_page_special_offers(request),
            'page_feedbacks': self._get_page_feedbacks(request),
            'feedbacks_stats': self._get_feedbacks_stats()
        }

    def _get_dealership_images(self) -> list[HomepageImage]:
        """Получает картинки для превью на главной страницы"""

        return HomepageImage.objects.all()

    def _get_page_special_offers(self, request: HttpRequest) -> Page[Car]:
        """Получает объект Page специальных предложений"""

        page_number = request.GET.get('special_offers_page')
        queryset = self.get_queryset_special_offers()
        return self.get_page_object(
            queryset, page_number, self.NUMBER_ITEM_PAGINATOR_SPECIAL_OFFERS
        )

    def get_queryset_special_offers(self) -> QuerySet[Car]:
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

    def _get_page_feedbacks(self, request: HttpRequest) -> Page[Feedback]:
        """Получает объект Page для отзывов"""

        page_number = request.GET.get('feedbacks_page')
        queryset = self.get_queryset_feedbacks()
        return self.get_page_object(
            queryset, page_number, self.NUMBER_ITEM_PAGINATOR_FEEDBACKS
        )

    def get_queryset_feedbacks(self) -> QuerySet[Feedback]:
        """Получает список отзывов"""

        return Feedback.objects.all().order_by('date_create')

    def _get_feedbacks_stats(self):
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
