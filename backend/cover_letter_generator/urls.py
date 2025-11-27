from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_cover_letter, name='api_cover_letter'),
]
