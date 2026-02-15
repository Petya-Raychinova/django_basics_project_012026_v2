from django.urls import path
from .views import index, bonus_report

app_name = "bonuspercent"

urlpatterns = [
    path("", index, name="index"), # форми за попълванв
    path("report/", bonus_report, name="bonus_report"), # отчет за % бонус
]