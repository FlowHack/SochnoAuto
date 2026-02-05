from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Prefetch
from django.shortcuts import render

from auto_store.models import Car, CarImage

from .models import Feedback, HomepageImage
from .settings import (NUMBER_ITEM_PAGINATOR_FEEDBACKS,
                       NUMBER_ITEM_PAGINATOR_SPECIAL_OFFERS)


def index(request):
    """Главная страница."""
    dealership_images = HomepageImage.objects.all()

    special_offers_qs = Car.objects.filter(
        is_special_offer=True, sold=False
    ).order_by('date_is_special_offer').prefetch_related(
        Prefetch(
            'car_images',
            CarImage.objects.order_by('order_image'),
            to_attr='ordered_images'
        )
    )
    special_offers_page = request.GET.get('special_offers_page')
    paginator_special_offers = Paginator(
        special_offers_qs, NUMBER_ITEM_PAGINATOR_SPECIAL_OFFERS
    )
    try:
        page_special_offers = paginator_special_offers.get_page(
            special_offers_page
        )
    except PageNotAnInteger:
        page_special_offers = paginator_special_offers.page(1)
    except EmptyPage:
        page_special_offers = paginator_special_offers.page(
            paginator_special_offers.num_pages
        )

    feedbacks_stats = Feedback.objects.aggregate(
        avg_score=Avg('score'), count_feedbacks=Count('id')
    )
    feedbacks = Feedback.objects.all()
    feedbacks_page = request.GET.get('feedbacks_page')
    paginator_feedbacks = Paginator(
        feedbacks, NUMBER_ITEM_PAGINATOR_FEEDBACKS
    )
    try:
        page_feedbacks = paginator_feedbacks.get_page(feedbacks_page)
    except PageNotAnInteger:
        page_feedbacks = paginator_feedbacks.page(1)
    except EmptyPage:
        page_feedbacks = paginator_feedbacks.page(
            paginator_feedbacks.num_pages
        )
    avg_rating = (
        round(feedbacks_stats['avg_score'], 1)
        if feedbacks_stats['avg_score'] is not None
        else None
    )

    context = {
        'dealership_images': dealership_images,
        'page_special_offers': page_special_offers,
        'page_feedbacks': page_feedbacks,
        'feedbacks_count': feedbacks_stats['count_feedbacks'],
        'avg_rating': avg_rating,
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
