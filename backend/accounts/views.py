from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import JobSeeker
from .serializers import JobSeekerSerializer, LoginSerializer

# Vue pour inscription
class RegisterView(generics.CreateAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Récupérer le rôle envoyé par la requête
        role = self.request.data.get('role', None)
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
