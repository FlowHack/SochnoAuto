from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
