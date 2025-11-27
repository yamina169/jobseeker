# profiles/views.py - Corrections complètes

from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, FileResponse
from datetime import datetime

# Import correct selon votre structure
from accounts.models import JobSeeker
from .models import Experience, Formation, Skill, CVHistory, PersonalInfo, Language, Project, Certification
from .serializers import (ExperienceSerializer, FormationSerializer, SkillSerializer, 
                         CVHistorySerializer, PersonalInfoSerializer, LanguageSerializer, 
                         ProjectSerializer, CertificationSerializer)
from .utils import profile_completeness
from .pdf_service import PDFGenerator

# Views corrigées - JobSeeker EST l'utilisateur
class PersonalInfoViewSet(viewsets.ModelViewSet):
    serializer_class = PersonalInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # JobSeeker est l'utilisateur connecté directement
        return PersonalInfo.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        try:
            personal_info = PersonalInfo.objects.get(user=request.user)
            serializer = self.get_serializer(personal_info)
            return Response([serializer.data])
        except PersonalInfo.DoesNotExist:
            return Response([])

    def retrieve(self, request, *args, **kwargs):
        try:
            personal_info = PersonalInfo.objects.get(user=request.user, id=kwargs['pk'])
            serializer = self.get_serializer(personal_info)
            return Response(serializer.data)
        except PersonalInfo.DoesNotExist:
            raise Http404

    def create(self, request, *args, **kwargs):
        try:
            # Vérifier si existe déjà
            if hasattr(request.user, 'personal_info'):
                personal_info = request.user.personal_info
                serializer = self.get_serializer(personal_info, data=request.data)
            else:
                serializer = self.get_serializer(data=request.data)
            
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LanguageViewSet(viewsets.ModelViewSet):
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Language.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CertificationViewSet(viewsets.ModelViewSet):
    serializer_class = CertificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Certification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Correction des views existantes aussi
class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FormationViewSet(viewsets.ModelViewSet):
    serializer_class = FormationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Formation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Views pour CV (corrigées aussi)
class UploadCVView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if 'cv' not in request.FILES:
                return Response({"error": "Aucun fichier fourni"}, status=status.HTTP_400_BAD_REQUEST)
            
            cv_file = request.FILES['cv']
            
            # Sauvegarder dans l'historique
            CVHistory.objects.create(
                user=request.user,
                cv=cv_file,
                file_name=cv_file.name
            )
            
            # Mettre à jour le CV actuel
            request.user.cv = cv_file
            request.user.save()
            
            return Response({"message": "CV uploadé avec succès"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CVHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cv_history = CVHistory.objects.filter(user=request.user).order_by('-uploaded_at')
            serializer = CVHistorySerializer(cv_history, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DownloadCVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, cv_id):
        try:
            cv_history = CVHistory.objects.get(id=cv_id, user=request.user)
            response = FileResponse(cv_history.cv.open(), as_attachment=True, filename=cv_history.file_name)
            return response
        except CVHistory.DoesNotExist:
            return Response({"error": "CV non trouvé"}, status=status.HTTP_404_NOT_FOUND)

# View pour la complétude
class ProfileCompletenessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            percentage = profile_completeness(request.user)
            return Response({'completeness': percentage})
        except Exception as e:
            print(f"Erreur complétude: {e}")
            return Response({'completeness': 0})

# Vue pour générer le PDF (corrigée aussi)
class GenerateCVPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            
            # Récupérer toutes les données du profil
            user_data = {
                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                },
                'personal_info': self.get_personal_info(user),
                'experiences': self.get_experiences(user),
                'formations': self.get_formations(user),
                'skills': self.get_skills(user),
                'languages': self.get_languages(user),
                'projects': self.get_projects(user),
                'certifications': self.get_certifications(user),
            }
            
            # Générer le PDF
            pdf_generator = PDFGenerator()
            pdf_buffer = pdf_generator.generate_cv_pdf(user_data)
            
            # Retourner le PDF en réponse
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            filename = f"CV_{user.first_name}_{user.last_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except Exception as e:
            print(f"Erreur génération PDF: {e}")
            return Response({"error": "Erreur lors de la génération du PDF"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_personal_info(self, user):
        try:
            personal_info = PersonalInfo.objects.get(user=user)
            return PersonalInfoSerializer(personal_info).data
        except PersonalInfo.DoesNotExist:
            return {}

    def get_experiences(self, user):
        experiences = user.experiences.all()
        return ExperienceSerializer(experiences, many=True).data

    def get_formations(self, user):
        formations = user.formations.all()
        return FormationSerializer(formations, many=True).data

    def get_skills(self, user):
        skills = user.skills.all()
        return SkillSerializer(skills, many=True).data

    def get_languages(self, user):
        languages = user.languages.all()
        return LanguageSerializer(languages, many=True).data

    def get_projects(self, user):
        projects = user.projects.all()
        return ProjectSerializer(projects, many=True).data

    def get_certifications(self, user):
        certifications = user.certifications.all()
        return CertificationSerializer(certifications, many=True).data