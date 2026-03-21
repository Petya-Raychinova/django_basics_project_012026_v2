import openpyxl
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UploadSalesQTY
from bonuspromo.models import PromoConditionsPercent, SalesQTY


def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadSalesQTY(request.POST, request.FILES)
        imported_rows_count = 0
        skipped_rows_count = 0

        if form.is_valid():
            excel_file = form.cleaned_data["upload_file_promo_qty"]
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            imported_rows = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                product_id = str(row[0]).strip() if row[0] else ""
                sold_qty = row[1]

                # ако няма стойности в реда
                if not product_id or not sold_qty:
                    skipped_rows_count += 1
                    continue

                condition = PromoConditionsPercent.objects.filter(product_id=product_id).first()

                if not condition:
                    skipped_rows_count += 1
                    continue

                SalesQTY.objects.create(
                    product_id=condition,
                    sold_qty=sold_qty
                )

                imported_rows_count += 1

            messages.success(request, "Импорт завършен.", extra_tags="import")
            messages.success(
                request,
                f"Импортирани в базата: {imported_rows_count} брой реда | "
                f"Пропуснати: {skipped_rows_count} брой реда поради несъществуващ продукт като кондиция. Въведи първо % компенсация!"
            )

            return redirect("import_promo_qty:index")

    else:
        form = UploadSalesQTY()

    return render(request, "import_promo_qty/index.html", {"form": form})