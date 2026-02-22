from django.urls import path

from .views import CategoryView, OfferView

app_name = 'cars'

urlpatterns = [
    path('', CategoryView.as_view(), name='categories'),
    path('offer/<slug:slug>/', OfferView.as_view(), name='offer')
]
