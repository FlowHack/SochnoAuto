from django.urls import path

from .views import get_cars_in_category, get_feedbacks, get_special_offers

urlpatterns = [
    path('v1/get-feedbacks', get_feedbacks, name='get_feedbacks'),
    path(
        'v1/get-special-offers', get_special_offers,
        name='get_special_offers'
    ),
    path(
        'v1/get-cars-in-category', get_cars_in_category,
        name='get_cars_in_category'
    )
]
