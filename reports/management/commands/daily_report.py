from django.core.management.base import BaseCommand
from reports.services import generate_report

class Command(BaseCommand):
    help = "Send daily bonus report"

    def handle(self, *args, **kwargs):
        result = generate_report()
        self.stdout.write(self.style.SUCCESS(result))