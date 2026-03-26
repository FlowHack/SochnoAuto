from django.shortcuts import render
from django.views import View

from core.cache import CACHE_CAR_DETAIL, method_cache_page_if_not_debug

from .services import CarService, CategoryService

CACHE_CATEGORY_LIST = 60 * 60


class CategoryView(View):
    """Класс для работы со страницей категорий"""

    def get(self, request):
        context = CategoryService().get_context(request)

        return render(request, 'cars/categories.html', context)


class CarView(View):
    """Класс для работы со странице автомобиля"""

    @method_cache_page_if_not_debug(CACHE_CAR_DETAIL)
    def get(self, request, slug: str):
        context = CarService().get_context(slug)

        return render(request, 'cars/car.html', context)
