"""
URL configuration for jobseeker_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include

from accounts.views import activate_user_view

from jobseeker_backend.matching.views import ResumeMatchingAPI


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')), 
    path('activate/<uidb64>/<token>/', activate_user_view, name='activate'),
path('api/scraper/', include('scraper.urls')),
    path("api/matching/", ResumeMatchingAPI.as_view(), name="resume_matching"),


]
