from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import JobSeeker

# Serializer pour inscription
class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ['email', 'first_name', 'last_name', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = JobSeeker(**validated_data)
        user.set_password(password)
        user.is_active = True  # Activer le compte automatiquement
        user.save()

        # Envoi d'un email de bienvenue (sans activation)
        html_content = render_to_string(
            'emails/welcome.html',  # Crée ce template
            {'user': user, 'year': now().year}
        )

        send_mail(
            'Bienvenue sur JobSeeker !',
            '',  # Message texte vide, HTML utilisé
            'ouniichayma@gmail.com',
            [user.email],
            html_message=html_content
        )
        return user

# Serializer pour login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Valide les identifiants et retourne l’utilisateur
        """
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Email ou mot de passe incorrect")
