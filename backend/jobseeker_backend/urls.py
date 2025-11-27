from django.contrib import admin
from django.urls import path, include
from jobseeker_backend.matching.views import ResumeMatchingAPI
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import os
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')), 
    path('api/scraper/', include('scraper.urls')),
    path("api/matching/", ResumeMatchingAPI.as_view(), name="resume_matching"),
    path('api/cover_letter/', include('cover_letter_generator.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        '/cover_letter_generator/document/',
        document_root=os.path.join(settings.BASE_DIR, 'cover_letter_generator', 'document')
    )