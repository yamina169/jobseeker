# profiles/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ExperienceViewSet, FormationViewSet, SkillViewSet,
    ProfileCompletenessView, UploadCVView, CVHistoryView, DownloadCVView,
    PersonalInfoViewSet, LanguageViewSet, ProjectViewSet, CertificationViewSet,
    GenerateCVPDFView
)

router = DefaultRouter()
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'formations', FormationViewSet, basename='formation')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'personal-info', PersonalInfoViewSet, basename='personal-info')
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'certifications', CertificationViewSet, basename='certification')

urlpatterns = router.urls + [
    path('completeness/', ProfileCompletenessView.as_view(), name='profile-completeness'),
    path('upload-cv/', UploadCVView.as_view(), name='upload-cv'),
    path('cv-history/', CVHistoryView.as_view(), name='cv-history'),
    path('download-cv/<int:cv_id>/', DownloadCVView.as_view(), name='download-cv'),
    path('generate-cv-pdf/', GenerateCVPDFView.as_view(), name='generate-cv-pdf'),
]