from django.urls import path
from .views import (
    RunEmploitunisieView,
    RunFarojobView,
    RunKeejobView,
    GetJobsFromCSV
  
)

urlpatterns = [
    path("run-emploitunisie/", RunEmploitunisieView.as_view(), name="run_emploitunisie"),
    path("run-farojob/", RunFarojobView.as_view(), name="run_farojob"),
    path("run-keejob/", RunKeejobView.as_view(), name="run_keejob"),
    path("jobs/", GetJobsFromCSV.as_view(), name="get_jobs_from_csv"),

]
