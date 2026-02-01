from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


def categories(request):
    """Страница категорий с фильтром по выбранной категории."""
    context = {
        'categories': [],  # Список категорий из БД
        'selected_category': None,
        'autos': [],
        'page_obj': None,
    }
    return render(request, 'auto_store/categories.html', context)


def offer(request, slug=None, pk=None):
    """Страница предложения (автомобиля)."""
    # Получите объект из БД по slug или pk
    offer_obj = None  # get_object_or_404(Offer, slug=slug) или pk=pk
    context = {
        'offer': offer_obj or {
            'id': pk or slug,
            'slug': slug or pk,
            'stamp': 'Марка',
            'model': 'Модель',
            'year': 2024,
            'mileage': 50000,
            'price': 1500000,
            'photos': [],
            'description': '',
            'specs': [],
        },
    }
    return render(request, 'auto_store/offer.html', context)


@require_POST
def order_request(request, slug=None, pk=None):
    """Обработка запроса на автотеку (добавление в БД)."""
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()

    if not name or not email:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Заполните все поля'}, status=400)
        return redirect('auto_store:offer_pk', pk=pk) if pk else redirect('auto_store:offer', slug=slug)

    # TODO: сохранить в БД
    # OrderRequest.objects.create(name=name, email=email, offer_id=...)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('auto_store:offer_pk', pk=pk) if pk else redirect('auto_store:offer', slug=slug)
