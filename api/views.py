from typing import TypeVar

from django.http import HttpRequest
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from cars.services import CarService, CategoryService
from core.cache import (CACHE_CATEGORY_CARS, CACHE_FEEDBACKS,
                        CACHE_SPECIAL_OFFERS, method_cache_page_if_not_debug)
from homepage.services import IndexService

T = TypeVar('T')


class SpecialOffersAPIView(APIView):
    """Получение списка специальных предложений (автомобилей со скидкой)"""

    @extend_schema(
        summary='Специальные предложения',
        description=(
            'Возвращает список автомобилей со статусом специального'
            'предложения'
        ),
        parameters=[
            OpenApiParameter(
                name='special_offers_page',
                description='Номер страницы для пагинации',
                required=False,
                type=int
            ),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'page': {
                        'type': 'object',
                        'properties': {
                            'object_list': {
                                'type': 'array',
                                'items': {'type': 'object'}
                            },
                            'number': {'type': 'integer'},
                            'num_pages': {'type': 'integer'}
                        }
                    },
                    'has_pages': {
                        'type': 'object',
                        'properties': {
                            'has_next': {'type': 'boolean'},
                            'has_previous': {'type': 'boolean'}
                        }
                    }
                }
            }
        }
    )
    @method_cache_page_if_not_debug(CACHE_SPECIAL_OFFERS)
    def get(self, request: HttpRequest) -> Response:
        return Response(IndexService().get_page_special_offers(request, False))


class FeedbacksAPIView(APIView):
    """Получение списка отзывов"""

    @extend_schema(
        summary="Отзывы",
        description="Возвращает список отзывов с пагинацией",
        parameters=[
            OpenApiParameter(
                name='feedbacks_page',
                description='Номер страницы для пагинации',
                required=False,
                type=int
            ),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'page': {
                        'type': 'object',
                        'properties': {
                            'object_list': {
                                'type': 'array',
                                'items': {'type': 'object'}
                            },
                            'number': {'type': 'integer'},
                            'num_pages': {'type': 'integer'}
                        }
                    },
                    'has_pages': {
                        'type': 'object',
                        'properties': {
                            'has_next': {'type': 'boolean'},
                            'has_previous': {'type': 'boolean'}
                        }
                    }
                }
            }
        }
    )
    @method_cache_page_if_not_debug(CACHE_FEEDBACKS)
    def get(self, request: HttpRequest) -> Response:
        return Response(IndexService().get_page_feedbacks(request, False))


class CategoryAPIView(APIView):
    """Получение списка автомобилей в категории"""

    @extend_schema(
        summary='Автомобили в категории',
        description=(
            'Возвращает список автомобилей выбранной категории с'
            'пагинацией'
        ),
        parameters=[
            OpenApiParameter(
                name='category',
                description='Slug категории автомобилей',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name='page',
                description='Номер страницы для пагинации',
                required=False,
                type=int
            ),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'page': {
                        'type': 'object',
                        'properties': {
                            'object_list': {
                                'type': 'array',
                                'items': {'type': 'object'}
                            },
                            'number': {'type': 'integer'},
                            'num_pages': {'type': 'integer'}
                        }
                    },
                    'has_pages': {
                        'type': 'object',
                        'properties': {
                            'has_next': {'type': 'boolean'},
                            'has_previous': {'type': 'boolean'}
                        }
                    }
                }
            }
        }
    )
    @method_cache_page_if_not_debug(CACHE_CATEGORY_CARS)
    def get(self, request: HttpRequest) -> Response:
        return Response(
            CategoryService().get_page_cars_in_category(
                request, None, False
            )
        )


class SearchCarAPIView(APIView):
    """Поиск автомобилей по марке, модели или году выпуска"""

    @extend_schema(
        summary='Поиск автомобилей',
        description=(
            'Поиск автомобилей по названию (марка, модель) или году выпуска'
        ),
        parameters=[
            OpenApiParameter(
                name='search',
                description='Поисковый запрос (марка, модель или год выпуска)',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name='page',
                description='Номер страницы для пагинации',
                required=False,
                type=int
            ),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'page': {
                        'type': 'object',
                        'properties': {
                            'object_list': {
                                'type': 'array',
                                'items': {'type': 'object'}
                            },
                            'number': {'type': 'integer'},
                            'num_pages': {'type': 'integer'}
                        }
                    },
                    'has_pages': {
                        'type': 'object',
                        'properties': {
                            'has_next': {'type': 'boolean'},
                            'has_previous': {'type': 'boolean'}
                        }
                    }
                }
            }
        }
    )
    def get(self, request: HttpRequest) -> Response:
        return Response(CarService().get_search_cars_page(request))
