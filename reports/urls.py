from django.urls import path
from .views import send_report_view

urlpatterns = [
    path("send-report/", send_report_view, name="send_report"),
]