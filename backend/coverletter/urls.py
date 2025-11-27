# coverletter/urls.py
from django.urls import path
from .views import GenerateLetterFromBestJobAPI


urlpatterns = [
    path("generate/", GenerateLetterFromBestJobAPI.as_view(), name="generate_letter"),
    

]
