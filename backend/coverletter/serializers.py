# coverletter/serializers.py
from rest_framework import serializers

class GenerateLetterSerializer(serializers.Serializer):
    resume = serializers.FileField(required=False)
    job_id = serializers.IntegerField(required=False)
    job = serializers.JSONField(required=False)
    length = serializers.ChoiceField(choices=["courte","moyenne","longue"], default="moyenne")
    tone = serializers.CharField(default="professionnel")
