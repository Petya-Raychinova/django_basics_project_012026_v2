import openpyxl
from celery import shared_task
from io import BytesIO

from bonuspercent.models import ConditionsPercent, PurchasingAmount


@shared_task
def process_purchasing_import(file_bytes):
    wb = openpyxl.load_workbook(BytesIO(file_bytes))
    sheet = wb.active

    imported_rows = 0
    skipped_rows = 0

    for row in sheet.iter_rows(min_row=2, values_only=True):
        eik = str(row[0]).strip() if row[0] else ""
        purchasing_amount = row[1]

        if not eik or not purchasing_amount:
            skipped_rows += 1
            continue

        condition = ConditionsPercent.objects.filter(eik=eik).first()

        if not condition:
            skipped_rows += 1
            continue

        PurchasingAmount.objects.create(
            condition_eik=condition,
            purchasing_amount=purchasing_amount
        )

        imported_rows += 1

    return f"Imported: {imported_rows}, Skipped: {skipped_rows}"