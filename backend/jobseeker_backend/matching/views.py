from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .logic import match_resume_with_jobs
import tempfile, os
import os
from django.conf import settings
class ResumeMatchingAPI(APIView):
    """
    POST /api/matching/
    Envoie un CV (PDF) et retourne les offres les plus pertinentes.
    """
    def post(self, request):
        resume_file = request.FILES.get("resume")
        if not resume_file:
            return Response({"error": "Aucun fichier PDF fourni"}, status=status.HTTP_400_BAD_REQUEST)

        # Sauvegarde temporaire du CV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            for chunk in resume_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            csv_path = os.path.join(settings.BASE_DIR, "data", "all_jobs_combined.csv")
            results = match_resume_with_jobs(tmp_path, csv_path, top_n=10)
            os.remove(tmp_path)
            return Response(results.to_dict(orient="records"))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
