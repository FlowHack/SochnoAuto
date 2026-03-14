from django.urls import path

from .views import CarView, CategoryView

app_name = 'cars'

urlpatterns = [
    path('category/', CategoryView.as_view(), name='category'),
    path('car/<slug:slug>/', CarView.as_view(), name='car')
]
