from django.core.management.base import BaseCommand
from reports.services import generate_report

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        report = generate_report()
        print(report)