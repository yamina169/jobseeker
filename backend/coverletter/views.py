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
            csv_path = os.path.join(settings.BASE_DIR, "data", "offres_brutes", "all_jobs_combined.csv")
            ranked_jobs = match_resume_with_jobs(tmp_path, csv_path, top_n=10)

            # Génération lettre pour le job le mieux classé
            letter = generate_cover_letter_from_job(tmp_path, ranked_jobs, job_index=0)

            os.remove(tmp_path)
            return Response({"letter": letter, "top_jobs": ranked_jobs.to_dict(orient="records")})

        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return Response({"error": str(e)}, status=500)




class GenerateLetterFromStoredDataAPI(APIView):
    """
    POST /api/coverletter/from-stored/
    Génère une lettre de motivation à partir d’un CV et d’un job déjà stockés en base.
    """
    def post(self, request):
        resume_id = request.data.get("resume_id")
        job_id = request.data.get("job_id")

        if not resume_id or not job_id:
            return Response({"error": "resume_id et job_id sont obligatoires"}, status=400)

        # Récupérer les données stockées
        
        from jobseeker_backend.matching.models import ResumeData, MatchedJob


        try:
            resume = ResumeData.objects.get(id=resume_id)
            job = MatchedJob.objects.get(id=job_id, resume=resume)
        except ResumeData.DoesNotExist:
            return Response({"error": "CV non trouvé"}, status=404)
        except MatchedJob.DoesNotExist:
            return Response({"error": "Job non trouvé pour ce CV"}, status=404)

        # Convertir en DataFrame pour compatibilité avec ta logique
        import pandas as pd

        ranked_jobs = pd.DataFrame([{
            "title": job.title,
            "company": job.company,
            "region": job.region,
            "description": job.description,
            "skills": job.skills
        }])

        # Générer la lettre
        from .utils.generator import generate_cover_letter_from_job

        letter = generate_cover_letter_from_job(
            cv_text=resume.extracted_text, 
            ranked_jobs=ranked_jobs,
            job_index=0
        )
        

        return Response({
            "letter": letter,
            "job_used": ranked_jobs.iloc[0].to_dict()
        })
