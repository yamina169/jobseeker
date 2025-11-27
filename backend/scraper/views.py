from rest_framework.views import APIView
from rest_framework.response import Response
import subprocess
import sys
from pathlib import Path
import json

SCRAPER_PATH = Path("scraper/scripts")
FUSION_SCRIPT = SCRAPER_PATH / "fusion_csv.py"

SCRAPERS = {
    "emploitunisie": SCRAPER_PATH / "emploitunisie_scraper.py",
    "farojob": SCRAPER_PATH / "farojob_scraper.py",
    "keejob": SCRAPER_PATH / "keejob_scraper.py",
}

def run_subprocess(script_path):
    """
    Exécute un script Python par subprocess et retourne dict {returncode, stdout, stderr}
    """
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    return {
        "returncode": res.returncode,
        "stdout": res.stdout or "",
        "stderr": res.stderr or ""
    }

def parse_fusion_result(stdout_text):
    """
    Le script fusion_csv.py imprime des logs puis un JSON final.
    Cette fonction cherche la dernière ligne JSON et la parse.
    """
    if not stdout_text:
        return None
    lines = [l.strip() for l in stdout_text.splitlines() if l.strip()]
    # chercher de la dernière ligne qui commence par '{'
    for line in reversed(lines):
        if line.startswith("{") and line.endswith("}"):
            try:
                return json.loads(line)
            except Exception:
                continue
    return None


class RunEmploitunisieView(APIView):
    def get(self, request):
        scraper_path = SCRAPERS["emploitunisie"]
        scraper_res = run_subprocess(scraper_path)

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
        scraper_path = SCRAPERS["farojob"]
        scraper_res = run_subprocess(scraper_path)

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
        scraper_path = SCRAPERS["keejob"]
        scraper_res = run_subprocess(scraper_path)

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
