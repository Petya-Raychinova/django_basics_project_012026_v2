from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bonus-report/", views.bonus_report, name="bonus_report"),
]