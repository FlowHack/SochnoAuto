from django.urls import path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

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
        'v1/search-car/', SearchCarAPIView.as_view(),
        name='search_car'
    ),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
]
