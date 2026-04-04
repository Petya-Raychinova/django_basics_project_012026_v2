from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from reports.services import generate_report
from django.contrib.auth.decorators import login_required


@login_required
def send_report_view(request):
    generate_report(request.user.email)

    messages.success(request, "Отчетът е изпратен успешно.")
    return redirect("nav")

