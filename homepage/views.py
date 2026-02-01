from django.shortcuts import render


def index(request):
    """Главная страница."""
    # special_offers_chunks: список чанков по 3 предложения [[o1,o2,o3], [o4,...]]
    # Можно передать special_offers и разбить: chunks = [offers[i:i+3] for i in range(0, len(offers), 3)]
    context = {
        'dealership_images': [],  # Список URL или {'url': ..., 'caption': ...}
        'special_offers_chunks': [],
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
