from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Prefetch
from django.shortcuts import render

from auto_store.models import Car, CarImage

from .models import Feedback, HomepageImage
from .settings import NUMBER_ITEM_PAGINATOR_FEEDBACKS


def index(request):
    """Главная страница."""
    dealership_images = HomepageImage.objects.all()

    special_offers_qs = Car.objects.filter(
        is_special_offer=True, sold=False
    ).order_by('-id').prefetch_related(
        Prefetch(
            'car_images',
            CarImage.objects.order_by('order_image'),
            to_attr='ordered_images'
        )
    )
    special_offers = list(special_offers_qs)
    chunks = [
        special_offers[i:i + 3] for i in range(0, len(special_offers), 3)
    ]

    feedbacks_stats = Feedback.objects.aggregate(
        avg_score=Avg('score'), count_feedbacks=Count('id')
    )
    feedbacks = Feedback.objects.all()
    feedbacks_page = request.GET.get('feedbacks_page')
    paginator = Paginator(feedbacks, NUMBER_ITEM_PAGINATOR_FEEDBACKS)
    try:
        page_feedbacks = paginator.get_page(feedbacks_page)
    except PageNotAnInteger:
        page_feedbacks = paginator.page(1)
    except EmptyPage:
        page_feedbacks = paginator.page(paginator.num_pages)

    context = {
        'dealership_images': dealership_images,
        'special_offers_chunks': chunks,
        'page_feedbacks': page_feedbacks,
        'feedbacks_count': feedbacks_stats['count_feedbacks'],
        'avg_rating': round(feedbacks_stats['avg_score'], 1),
    }
    return render(request, 'homepage/index.html', context)


def contacts(request):
    """Страница контактов."""
    context = {
        # Переопределите в своём шаблоне или передайте из view:
        # 'phone': '+7 (999) 123-45-67',
        # 'telegram_url': 'https://t.me/your_channel',
    }
    return render(request, 'homepage/contacts.html', context)
