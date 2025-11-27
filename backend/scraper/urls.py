from django.urls import path
from .views import (
    RunEmploitunisieView,
    RunFarojobView,
    RunKeejobView,
  
)

urlpatterns = [
    path("run-emploitunisie/", RunEmploitunisieView.as_view(), name="run_emploitunisie"),
    path("run-farojob/", RunFarojobView.as_view(), name="run_farojob"),
    path("run-keejob/", RunKeejobView.as_view(), name="run_keejob"),
]
