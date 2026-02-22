from django.shortcuts import render
from django.views import View

from .services import IndexService


class IndexView(View, IndexService):
    """View класс для отрисовки главной страницы"""

    def get(self, request):
        context = self.get_index_context(request)
        return render(request, 'homepage/index.html', context=context)
