from django.urls import path

from .views import (CategoryAPIView, FeedbacksAPIView, SearchCarAPIView,
                    SpecialOffersAPIView)

app_name = 'api'

urlpatterns = [
    path(
        'v1/special-offers/', SpecialOffersAPIView.as_view(),
        name='special_offers'
    ),
    path(
        'v1/feedbacks/', FeedbacksAPIView.as_view(),
        name='feedbacks'
    ),
    path(
        'v1/category/', CategoryAPIView.as_view(),
        name='category'
    ),
    path(
        'web1/search-car/', SearchCarAPIView.as_view(),
        name='search_car'
    )
]
