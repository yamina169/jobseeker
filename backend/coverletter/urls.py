# coverletter/urls.py
from django.urls import path
from .views import GenerateLetterFromBestJobAPI,GenerateLetterFromStoredDataAPI



urlpatterns = [
    path("generate/", GenerateLetterFromBestJobAPI.as_view(), name="generate_letter"),
      path("generate/from-stored/", GenerateLetterFromStoredDataAPI.as_view(), name="generate_letter_from-stored")

]
