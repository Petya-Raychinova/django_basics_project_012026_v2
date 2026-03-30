from django.http import HttpResponse
from reports.services import generate_report
from django.contrib.auth.decorators import login_required


@login_required
def send_report_view(request):
    result = generate_report()
    return HttpResponse(result)


