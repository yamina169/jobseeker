from django.db import models


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Manager pour créer les utilisateurs
class JobSeekerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Création d'un utilisateur standard
        """
        if not email:
            raise ValueError('L’utilisateur doit avoir un email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashage sécurisé du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Création de l’administrateur
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # rôle admin
        return self.create_user(email, password, **extra_fields)

# Définition du modèle JobSeeker
class JobSeeker(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('jobseeker', 'Job Seeker'),
        ('admin', 'Admin'),
    ]

    # Champs principaux
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='jobseeker')
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)  # PDF optionnel

    # Gestion Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Manager
    objects = JobSeekerManager()

    # Pour l’authentification
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"
