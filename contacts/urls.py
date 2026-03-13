from django.urls import path
from django.views.generic import TemplateView

from .views import ConfirmEmailView, RequestContactCreateView, contacts

app_name = 'contacts'

urlpatterns = [
    path('', contacts, name='contacts'),
    path('create/', RequestContactCreateView.as_view(), name='create'),
    path(
        'confirm/success/',
        TemplateView.as_view(template_name='contacts/success.html'),
        name='confirm_success'
    ),
    path(
        'confirm/error/',
        TemplateView.as_view(template_name='contacts/error.html'),
        name='confirm_error'
    ),
    path(
        'confirm/<uuid:token>/',
        ConfirmEmailView.as_view(),
        name='confirmation_email'
    ),
]
