from django.contrib import admin
from django.urls import path, include
from jobseeker_backend.matching.views import ResumeMatchingAPI

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')), 
    path('api/scraper/', include('scraper.urls')),
    path("api/matching/", ResumeMatchingAPI.as_view(), name="resume_matching"),
  path('api/profiles/', include('profiles.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)