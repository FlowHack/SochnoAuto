from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import BooleanField, Case, Value, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Car, CarCategory
from .settings import NUMBER_ITEM_PAGINATOR_CARS


def categories(request):
    """Страница категорий с фильтром по выбранной категории."""
    selected_category = request.GET.get('category')
    page = request.GET.get('page')

    categories = CarCategory.objects.annotate(
        selected_category=Case(
            When(slug=selected_category, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    )

    select_category = categories.filter(
        selected_category=True
    ).first()
    page_cars = None
    if select_category:
        cars = select_category.cars_in_category.all().prefetch_related(
            'car_images'
        )
        paginator = Paginator(cars, NUMBER_ITEM_PAGINATOR_CARS)
        try:
            page_cars = paginator.get_page(
                page
            )
        except PageNotAnInteger:
            page_cars = paginator.page(1)
        except EmptyPage:
            page_cars = paginator.page(
                paginator.num_pages
            )

    context = {
        'categories': categories,
        'page_cars': page_cars
    }
    return render(request, 'auto_store/categories.html', context)


def offer(request, slug=None):
    """Страница предложения (автомобиля)."""
    offer_obj = get_object_or_404(Car, slug=slug)

    context = {
        'offer': offer_obj
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
