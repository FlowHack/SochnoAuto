from django.urls import path

from .views import get_feedbacks, get_special_offers

urlpatterns = [
    path('v1/get-feedbacks', get_feedbacks, name='get_feedbacks'),
    path(
        'v1/get-special-offers', get_special_offers,
        name='get_special_offers'
    )
]
