from typing import TypeVar

from django.core.paginator import Page
from django.http import HttpRequest
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView

from cars.models import Car
from homepage.models import Feedback
from homepage.services import IndexService

T = TypeVar['T']


class PaginatedPartialsAPIView(APIView):
    """Абстрактный класс для отрисовки пагинированных данных"""

    template_cards = None
    template_pagination = None

    def get_page_data(self, request: HttpRequest) -> Page[T]:
        """Реализуется в дочерних классах, получает пагинированные данные

        Args:
            request (HttpRequest): Объект запроса

        Raises:
            NotImplementedError: Вызывается, если метод не был объявлен
                в дочернем классе

        Returns:
            Page[T]: Объект с пагинированными данными
        """

        raise NotImplementedError

    def get(self, request):
        page = self.get_page_data(request)

        html_cards = render_to_string(
            self.template_cards,
            {'page': page},
            request=request
        )
        html_pagination = render_to_string(
            self.template_pagination,
            {'page': page}
        )

        return Response(
            {
                'html_cards': html_cards,
                'html_pagination': html_pagination
            }
        )


class SpecialOffersAPIView(PaginatedPartialsAPIView):
    """Класс для обработки запросов по специальным предложениям"""

    template_cards = 'homepage/partials/cards_special_offers.html'
    template_pagination = 'homepage/partials/pagination_special_offers.html'

    def get_page_data(self, request: HttpRequest) -> Page[Car]:
        return IndexService().get_page_special_offers(request)


class FeedbacksAPIView(PaginatedPartialsAPIView):
    """Класс для обработки запросов по отзывам"""

    template_cards = 'homepage/partials/cards_feedbacks.html'
    template_pagination = 'homepage/partials/pagination_feedbacks.html'

    def get_page_data(self, request: HttpRequest) -> Page[Feedback]:
        return IndexService().get_page_feedbacks(request)
