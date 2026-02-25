from django.shortcuts import render
from django.views import View

from .services import CarService, CategoryService


class CategoryView(View):
    """Класс для работы со страницей категорий"""

    def get(self, request):
        category_slug = request.GET.get('category')
        page_number = request.GET.get('page')

        context = CategoryService().get_context(category_slug, page_number)

        return render(request, 'cars/categories.html', context)


class CarView(View):
    """Класс для работы со странице автомобиля"""

    def get(self, request, slug: str):
        context = CarService().get_context(slug)

        return render(request, 'cars/car.html', context)
