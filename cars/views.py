from django.shortcuts import render
from django.views import View

from .services import CategoryService


class CategoryView(View, CategoryService):
    """Класс для работы со страницей категорий"""

    def get(self, request):
        category_slug = request.GET.get('category')
        page_number = request.GET.get('page')

        context = self.get_context(category_slug, page_number)

        return render(request, 'cars/categories.html', context)


class OfferView(View):
    pass
