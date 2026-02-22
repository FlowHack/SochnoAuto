from django.urls import path
from .views import SpecialOffersAPIView, FeedbacksAPIView

app_name = 'api'

urlpatterns = [
    path(
        'v1/special-offers/', SpecialOffersAPIView.as_view(),
        name='special_offers'
    ),
    path(
        'v1/feedbacks/', FeedbacksAPIView.as_view(),
        name='feedbacks'
    )
]
