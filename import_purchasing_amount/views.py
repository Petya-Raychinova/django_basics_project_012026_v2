import openpyxl
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UploadPurchasingAmount
from bonuspercent.models import ConditionsPercent, PurchasingAmount


def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadPurchasingAmount(request.POST, request.FILES)

        if form.is_valid():
            excel_file = form.cleaned_data["upload_file"]
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            imported_rows = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                eik = str(row[0]).strip()
                purchasing_amount = row[1]

                try:


                    PurchasingAmount.objects.create(
                        eik=eik,
                        purchasing_amount=purchasing_amount
                    )

                    imported_rows += 1

                except ConditionsPercent.DoesNotExist:
                    continue

            messages.success(request, f"Импортирани успешно {imported_rows} редове.")
            return redirect("import_purchasing_amount:index")

    else:
        form = UploadPurchasingAmount()

    return render(request, "import_purchasing_amount/index.html", {"form": form})

