# accounts/backends.py
from django.contrib.auth.backends import BaseBackend
from .models import JobSeeker

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = JobSeeker.objects.get(email=email)
        except JobSeeker.DoesNotExist:
            return None
        if user.check_password(password) and user.is_active:
            return user
        return None

    def get_user(self, user_id):
        try:
            return JobSeeker.objects.get(pk=user_id)
        except JobSeeker.DoesNotExist:
            return None
