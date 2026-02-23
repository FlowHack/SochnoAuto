from django.urls import path

from .views import CategoryView, OfferView

app_name = 'cars'

urlpatterns = [
    path('category/', CategoryView.as_view(), name='category'),
    path('offer/<slug:slug>/', OfferView.as_view(), name='offer')
]
