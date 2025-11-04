from django.urls import path
from .views import ScrapeJobsView

urlpatterns = [
    path('run/', ScrapeJobsView.as_view(), name='run_scraper'),
]
