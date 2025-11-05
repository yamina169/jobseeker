from django.shortcuts import render

# Create your views here.


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import JobSeeker
from .serializers import JobSeekerSerializer, LoginSerializer






from allauth.account.views import SignupView
from rest_framework.views import APIView
from rest_framework.response import Response











# views.py
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import JobSeeker


from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import JobSeeker

def activate_user_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = JobSeeker.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'emails/activation_success.html', {'user': user})
    else:
        return render(request, 'emails/activation_failed.html')





class AllAuthRegisterView(SignupView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({"detail": "Email de confirmation envoyé si valide"})




# Vue pour inscription
# views.py
class RegisterView(generics.CreateAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Récupérer le rôle envoyé par la requête
        role = self.request.data.get('role', None)
        
        # Si aucun rôle n’est fourni, on assigne "jobseeker" par défaut
        if not role:
            role = 'jobseeker'

        serializer.save(role=role)


# Vue pour login
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # Génération des tokens JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role
        })

