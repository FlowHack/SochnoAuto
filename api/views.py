from typing import TypeVar

from django.core.paginator import Page
from django.db.models import QuerySet
from django.http import HttpRequest
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView

from cars.models import Car
from cars.services import CarService, CategoryService
from homepage.services import IndexService

T = TypeVar('T')


class PaginatedPartialsAPIView(APIView):
    """Абстрактный класс для отрисовки пагинированных данных"""

    template_cards = None
    template_pagination = None
    need_pagination = True

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
        response = {'html_cards': html_cards}

        if self.need_pagination:
            html_pagination = render_to_string(
                self.template_pagination,
                {'page': page}
            )
            response['html_pagination'] = html_pagination

        return Response(response)


class SpecialOffersAPIView(APIView):
    """Класс для обработки запросов по специальным предложениям"""

    def get(self, request: HttpRequest):
        return Response(IndexService().get_page_special_offers(request, False))


class FeedbacksAPIView(APIView):
    """Класс для обработки запросов по отзывам"""

    def get(self, request: HttpRequest):
        return Response(IndexService().get_page_feedbacks(request, False))


class CategoryAPIView(APIView):
    """Класс для обработки запросов по категориям"""

    def get(self, request: HttpRequest):
        return Response(
            CategoryService().get_page_cars_in_category(
                request, None, False
            )
        )


class SearchCarAPIView(PaginatedPartialsAPIView):
    """Класс для обработки поиска по автомобилям"""

    template_cards = 'partials/search_results.html'
    need_pagination = False

    def get_page_data(self, request: HttpRequest) -> Page[Car]:
        search_query = request.GET.get('search')
        if not search_query:
            return QuerySet()
        page_number = request.GET.get('page')

        return CarService().get_search_cars_page(search_query, page_number)
