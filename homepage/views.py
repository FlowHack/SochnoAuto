from django.db.models import Prefetch
from django.shortcuts import render

from auto_store.models import Car, CarImage


def index(request):
    """Главная страница."""
    special_offers_qs = Car.objects.filter(
        is_special_offer=True
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

    context = {
        'dealership_images': [],  # Список URL или {'url': ..., 'caption': ...}
        'special_offers_chunks': chunks,
        'feedbacks': [],
        'feedbacks_count': 0,
        'avg_rating': 5,
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
