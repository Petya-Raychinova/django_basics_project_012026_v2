from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.decorators import manager_required
from .forms import UploadPurchasingAmount
from .tasks import process_purchasing_import


@manager_required
def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadPurchasingAmount(request.POST, request.FILES)

        if form.is_valid():
            excel_file = request.FILES["upload_file"]

            try:
                #асинхронно (ако има Celery + Redis)
                process_purchasing_import.delay(excel_file.read())
                messages.success(request, "Импортът е стартиран (асинхронно).")

            except Exception:
                #ако Celery не работи (например в Azure)
                result = process_purchasing_import(excel_file.read())
                messages.success(request, f"Импортът завърши: {result}")

            return redirect("import_purchasing_amount:index")

    else:
        form = UploadPurchasingAmount()

    return render(request, "import_purchasing_amount/index.html", {"form": form})