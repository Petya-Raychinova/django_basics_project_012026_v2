import openpyxl
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UploadPurchasingAmount
from bonuspercent.models import ConditionsPercent, PurchasingAmount


def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadPurchasingAmount(request.POST, request.FILES)
        imported_rows_count = 0
        skipped_rows_count = 0

        if form.is_valid():
            excel_file = form.cleaned_data["upload_file"]
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            imported_rows = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                eik = str(row[0]).strip() if row[0] else ""
                purchasing_amount = row[1]

                # ако няма стойности в реда
                if not eik or not purchasing_amount:
                    skipped_rows_count += 1
                    continue

                condition = ConditionsPercent.objects.filter(eik=eik).first()

                if not condition:
                    skipped_rows_count += 1
                    continue

                PurchasingAmount.objects.create(
                    condition_eik=condition,
                    purchasing_amount=purchasing_amount
                )

                imported_rows_count += 1

            messages.success(request, "Импорт завършен.", extra_tags="import")
            messages.success(
                request,
                f"Импортирани в базата: {imported_rows_count} брой реда | Пропуснати: {skipped_rows_count} брой реда поради несъществуващ ЕИК като кондиция. Въведи първо % бонус!"
            )

            return redirect("import_purchasing_amount:index")

    else:
        form = UploadPurchasingAmount()

    return render(request, "import_purchasing_amount/index.html", {"form": form})

