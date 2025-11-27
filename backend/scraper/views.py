from rest_framework.views import APIView
from rest_framework.response import Response
import subprocess
import sys
from pathlib import Path
import json
import csv
import os
from django.conf import settings
import math


# -----------------------------
# PATHS
# -----------------------------
SCRAPER_PATH = Path("scraper/scripts")
FUSION_SCRIPT = SCRAPER_PATH / "fusion_csv.py"

SCRAPERS = {
    "emploitunisie": SCRAPER_PATH / "emploitunisie_scraper.py",
    "farojob": SCRAPER_PATH / "farojob_scraper.py",
    "keejob": SCRAPER_PATH / "keejob_scraper.py",
}

# NOUVEAU CHEMIN CSV (fix)
CSV_PATH = os.path.join(
    settings.BASE_DIR,
    "data", "offres_unifiees.csv"
)


# -----------------------------
# SUBPROCESS UTIL
# -----------------------------
def run_subprocess(script_path):
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    return {
        "returncode": res.returncode,
        "stdout": res.stdout or "",
        "stderr": res.stderr or ""
    }


def parse_fusion_result(stdout_text):
    if not stdout_text:
        return None
    lines = [l.strip() for l in stdout_text.splitlines() if l.strip()]
    for line in reversed(lines):
        if line.startswith("{") and line.endswith("}"):
            try:
                return json.loads(line)
            except:
                continue
    return None


# -----------------------------
# SCRAPER VIEWS
# -----------------------------
class RunEmploitunisieView(APIView):
    def get(self, request):
        scraper_res = run_subprocess(SCRAPERS["emploitunisie"])
        fusion_res = run_subprocess(FUSION_SCRIPT)
        fusion_info = parse_fusion_result(fusion_res["stdout"])
        return Response({
            "status": "ok" if scraper_res["returncode"] == 0 else "error",
            "scraper": "emploitunisie",
            "scraper_stdout": scraper_res["stdout"],
            "scraper_stderr": scraper_res["stderr"],
            "fusion_stdout": fusion_res["stdout"],
            "fusion_stderr": fusion_res["stderr"],
            "fusion_info": fusion_info
        })


class RunFarojobView(APIView):
    def get(self, request):
        scraper_res = run_subprocess(SCRAPERS["farojob"])
        fusion_res = run_subprocess(FUSION_SCRIPT)
        fusion_info = parse_fusion_result(fusion_res["stdout"])
        return Response({
            "status": "ok" if scraper_res["returncode"] == 0 else "error",
            "scraper": "farojob",
            "scraper_stdout": scraper_res["stdout"],
            "scraper_stderr": scraper_res["stderr"],
            "fusion_stdout": fusion_res["stdout"],
            "fusion_stderr": fusion_res["stderr"],
            "fusion_info": fusion_info
        })


class RunKeejobView(APIView):
    def get(self, request):
        scraper_res = run_subprocess(SCRAPERS["keejob"])
        fusion_res = run_subprocess(FUSION_SCRIPT)
        fusion_info = parse_fusion_result(fusion_res["stdout"])
        return Response({
            "status": "ok" if scraper_res["returncode"] == 0 else "error",
            "scraper": "keejob",
            "scraper_stdout": scraper_res["stdout"],
            "scraper_stderr": scraper_res["stderr"],
            "fusion_stdout": fusion_res["stdout"],
            "fusion_stderr": fusion_res["stderr"],
            "fusion_info": fusion_info
        })



class GetJobsFromCSV(APIView):
    """
    API qui lit le fichier CSV + permet recherche keyword & secteur + pagination
    """

    def get(self, request):
        if not os.path.exists(CSV_PATH):
            return Response({"error": "CSV file not found"}, status=404)

        # ----- Pagination -----
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
        except:
            page = 1
            limit = 10

        # ----- Filtres -----
        keyword = request.GET.get("keyword", "").strip().lower()
        sector_filter = request.GET.get("sector", "").strip().lower()

        jobs = []
        try:
            with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                all_rows = list(reader)

                # ----- 🔍 Recherche par mots-clés -----
                if keyword:
                    def match_keyword(job):
                        fields_to_check = [
                            "title", "company", "region", "sector",
                            "short_description", "full_description", "skills"
                        ]
                        for field in fields_to_check:
                            value = (job.get(field, "") or "").lower()
                            if keyword in value:
                                return True
                        return False

                    all_rows = [row for row in all_rows if match_keyword(row)]

                # ----- 🔎 Filtrer par secteur -----
                if sector_filter:
                    # Split sector_filter en plusieurs mots-clés envoyés depuis le frontend
                    sectors = [s.strip() for s in sector_filter.split(",") if s.strip()]
                    all_rows = [
                        row for row in all_rows
                        if any(s in (row.get("sector", "").lower()) for s in sectors)
                    ]

                # ----- Pagination -----
                total_jobs = len(all_rows)
                total_pages = (total_jobs + limit - 1) // limit

                start = (page - 1) * limit
                end = start + limit
                paginated = all_rows[start:end]

                # Nettoyer les données null
                for row in paginated:
                    jobs.append({k: (v if v else None) for k, v in row.items()})

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({
            "page": page,
            "limit": limit,
            "total_jobs": total_jobs,
            "total_pages": total_pages,
            "count": len(jobs),
            "jobs": jobs
        })
