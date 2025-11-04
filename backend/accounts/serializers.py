from rest_framework import serializers
from .models import JobSeeker
from django.contrib.auth import authenticate

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

# Serializer pour inscription
from django.template.loader import render_to_string
from django.utils.timezone import now

class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ['email', 'first_name', 'last_name', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = JobSeeker(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()

        request = self.context.get('request')
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        link = f"http://127.0.0.1:8000/activate/{uid}/{token}/"

        # Générer le contenu HTML
        html_content = render_to_string(
            'emails/activate.html',
            {'user': user, 'link': link, 'year': now().year}
        )

        send_mail(
            'Active ton compte JobSeeker',
            '',  # message texte vide, HTML sera utilisé
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
