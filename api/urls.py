from django.urls import path

from .views import get_feedbacks

urlpatterns = [
    path('v1/get-feedbacks', get_feedbacks, name='get_feedbacks')
]
