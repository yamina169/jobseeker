from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .logic import generate_cover_letter, create_pdf, extract_name_from_pdf
import os

@csrf_exempt
def api_cover_letter(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST method"}, status=405)

    cv_file = request.FILES.get("cv_file")
    job_description = request.POST.get("job_description")
    model_name = request.POST.get("model_name", "gemma3")

    if not cv_file or not job_description:
        return JsonResponse({"error": "Please provide cv_file and job_description"}, status=400)

    try:
        # Extraire le nom depuis le CV PDF
        name = extract_name_from_pdf(cv_file)
        if not name:
            name = "Applicant"

        # Générer la lettre
        cover_letter = generate_cover_letter(name, cv_file, job_description, model_name)

        # Créer PDF de la lettre
        pdf_dir = os.path.join(settings.BASE_DIR, 'cover_letter_generator', 'document')
        os.makedirs(pdf_dir, exist_ok=True)
        safe_name = name.replace(" ", "_")
        pdf_filename = f"{safe_name}_CoverLetter.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)

        create_pdf(cover_letter, pdf_path, f"{name} - Cover Letter")

        # Retourner le PDF dans le navigateur
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf',
                            filename=pdf_filename, as_attachment=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
