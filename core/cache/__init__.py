CACHE_SPECIAL_OFFERS = 60 * 5
CACHE_FEEDBACKS = 60 * 30
CACHE_CATEGORIES = 60 * 60
CACHE_CATEGORY_CARS = 60 * 5
CACHE_CAR_DETAIL = 60 * 60
CACHE_CONTACTS = 60 * 60


def cache_page_if_not_debug(timeout):
    """Декоратор для кэширования страниц. Отключает кэширование в
    DEBUG режиме."""
    def decorator(func):
        from django.conf import settings
        if settings.DEBUG:
            return func
        from django.views.decorators.cache import cache_page
        return cache_page(timeout)(func)
    return decorator


def method_cache_page_if_not_debug(timeout):
    """Декоратор для кэширования методов классовых представлений.
    Отключает кэширование в DEBUG режиме."""

    def decorator(func):
        from django.conf import settings
        if settings.DEBUG:
            return func
        from django.utils.decorators import method_decorator
        from django.views.decorators.cache import cache_page
        return method_decorator(cache_page(timeout))(func)
    return decorator
