from django.shortcuts import render
from django.views import View

from .services import IndexService


class IndexView(View, IndexService):
    """View класс для отрисовки главной страницы"""

    def get(self, request):
        context = self.get_index_context(request)
        return render(request, 'homepage/index.html', context=context)


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
