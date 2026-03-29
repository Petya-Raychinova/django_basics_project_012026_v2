from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.decorators import manager_required
from .forms import UploadPurchasingAmount
from .tasks import process_purchasing_import
from django.conf import settings


@manager_required
def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadPurchasingAmount(request.POST, request.FILES)

        if form.is_valid():
            excel_file = request.FILES["upload_file"]

            # асинхронно извикване
            if settings.IS_PRODUCTION:
                result = process_purchasing_import(excel_file.read())

                messages.success(request, f"Импортът завърши: {result}")
            else:
                process_purchasing_import.delay(excel_file.read())

                messages.success(request, "Импортът е стартиран (асинхронно).")



            return redirect("import_purchasing_amount:index")

    else:
        form = UploadPurchasingAmount()

    return render(request, "import_purchasing_amount/index.html", {"form": form})