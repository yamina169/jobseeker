import sys
from rest_framework.response import Response
from rest_framework.views import APIView
import subprocess

class ScrapeJobsView(APIView):
    def get(self, request):
        script_path = "scraper/scripts/scraper_jobs.py"
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)

        return Response({
            "status": "ok" if result.returncode == 0 else "error",
            "python_used": sys.executable,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "script_path": script_path
        })
