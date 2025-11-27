# coverletter/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import tempfile, os
from django.conf import settings



# Import depuis utils de coverletter
from .utils.generator import generate_cover_letter_from_job

# Import depuis jobseeker_backend/matching/logic.py
from jobseeker_backend.matching.logic import match_resume_with_jobs

class GenerateLetterFromBestJobAPI(APIView):
    """
    POST /api/coverletter/generate/
    Envoie un CV et génère automatiquement une lettre pour le job le mieux classé.
    """
    def post(self, request):
        resume_file = request.FILES.get("resume")
        if not resume_file:
            return Response({"error": "Aucun fichier PDF fourni"}, status=400)

        # Fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            for chunk in resume_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            # Matching
            csv_path = os.path.join(settings.BASE_DIR, "data", "offres_unifiees.csv")
            ranked_jobs = match_resume_with_jobs(tmp_path, csv_path, top_n=10)

            # Génération lettre pour le job le mieux classé
            letter = generate_cover_letter_from_job(tmp_path, ranked_jobs, job_index=0)

            os.remove(tmp_path)
            return Response({"letter": letter, "top_jobs": ranked_jobs.to_dict(orient="records")})

        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return Response({"error": str(e)}, status=500)




