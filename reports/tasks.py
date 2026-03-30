from celery import shared_task
from .services import generate_report

@shared_task
def send_daily_report():
    return generate_report()