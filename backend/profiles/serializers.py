from rest_framework import serializers
from .models import CVHistory, Certification, Experience, Formation, Language, PersonalInfo, Project, Skill

# profiles/serializers.py
from rest_framework import serializers
from accounts.models import JobSeeker

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ['user']


class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'
        read_only_fields = ['user']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ['user']


class CVUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ['cv']



class CVHistorySerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()
    uploaded_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    class Meta:
        model = CVHistory
        fields = ['id', 'file_name', 'uploaded_at', 'file_size', 'cv']

    def get_file_size(self, obj):
        if obj.cv and obj.cv.size:
            size = obj.cv.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        return "0 B"
    



class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = '__all__'
        read_only_fields = ['user']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
        read_only_fields = ['user']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['user']

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'
        read_only_fields = ['user']