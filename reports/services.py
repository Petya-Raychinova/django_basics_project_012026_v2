from openpyxl import Workbook
from django.core.mail import EmailMessage

def generate_report():
    from bonuspercent.models import ConditionsPercent, PurchasingAmount

    wb = Workbook()
    ws = wb.active
    ws.title = "Daily Report"

    ws.append(["EIK", "Amount", "Percent", "Bonus"])

    data = PurchasingAmount.objects.all()

    for row in data:
        eik = row.condition_eik.eik
        amount = row.purchasing_amount

        condition = ConditionsPercent.objects.filter(eik=eik).first()
        percent = condition.percent_condition if condition else 0
        bonus = amount * percent / 100

        ws.append([eik, float(amount), float(percent), float(bonus)])

    file_path = "daily_report.xlsx"
    wb.save(file_path)

    #мейл
    email = EmailMessage(
        subject="Daily Bonus Report",
        body="В прикачения файл е дневният отчет за бонус от покупката.",
        from_email="petya.raychinova@gmail.com",
        to=["petya.raychinova@gmail.com"],
    )

    email.attach_file(file_path)
    email.send()

    return "Генериран отчет и изпратен мейл"