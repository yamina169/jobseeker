from django.contrib import admin
from django.urls import path, include
from jobseeker_backend.matching.views import ResumeMatchingAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')), 
    path('api/scraper/', include('scraper.urls')),
    path("api/matching/", ResumeMatchingAPI.as_view(), name="resume_matching"),
]
