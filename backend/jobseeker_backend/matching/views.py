from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .logic import match_resume_with_jobs
import tempfile, os
from django.conf import settings
from pathlib import Path

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
            # ← UTILISER LE FICHIER UNIFIÉ
            csv_path = Path(settings.BASE_DIR) / "data" / "offres_unifiees.csv"
            if not csv_path.exists():
                return Response({"error": "Fichier unifié introuvable"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            results = match_resume_with_jobs(tmp_path, csv_path, threshold=0.6)
            os.remove(tmp_path)
            return Response(results.to_dict(orient="records"))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
