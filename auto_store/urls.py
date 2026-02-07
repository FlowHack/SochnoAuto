from django.urls import path

from . import views

app_name = 'auto_store'

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('offer/<slug:slug>/', views.offer, name='offer'),
    path('offer/<slug:slug>/order/', views.order_request, name='order_request_slug'),
    path('offer/<int:pk>/order/', views.order_request, name='order_request_pk'),
]
