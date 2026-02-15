from http.client import HTTPResponse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum

from .forms import ConditionForm, PurchasingForm
from .models import ConditionsPercent, PurchasingAmount


def index(request: HttpRequest) -> HTTPResponse:
    condition_form = ConditionForm()
    purchasing_form = PurchasingForm()

    if request.method == "POST":
        if "add_condition" in request.POST:
            condition_form = ConditionForm(request.POST)
            if condition_form.is_valid():
                condition_form.save()
                return redirect("bonuspercent:index")

        elif "add_purchase" in request.POST:
            purchasing_form = PurchasingForm(request.POST)
            if purchasing_form.is_valid():
                eik = purchasing_form.cleaned_data["eik"]
                amount = purchasing_form.cleaned_data["purchasing_amount"]

                # запис по eik (БЕЗ condition)
                PurchasingAmount.objects.create(
                   eik=eik,
                    purchasing_amount=amount
                )
                return redirect("bonuspercent:index")

    return render(
        request,
        "bonuspercent\index.html",
        {
            "condition_form": condition_form,
            "purchasing_form": purchasing_form
        }
    )

def bonus_report(request: HttpRequest) -> HTTPResponse:
    # суми по доставчик
    purchases = (
        PurchasingAmount.objects
        .values("eik")
        .annotate(total_amount=Sum("purchasing_amount"))
    )

    # добавяне на процент и бонус (Python логика)
    report = []
    for p in purchases:
        condition = ConditionsPercent.objects.filter(eik=p["eik"]).first()

        if not condition:
            continue  # ако няма % бонус за този доставчик да не хвърля грешка, за да продължи. Като бизнес логика е ок

        bonus = p["total_amount"] * condition.percent_condition / 100
        report.append({
            "eik": p["eik"],
            "supplier_name": condition.supplier_name,
            "percent_condition": condition.percent_condition,
            "total_amount": p["total_amount"],
            "bonus": bonus,
        })

    return render(
        request,
        "bonuspercent/bonus_report.html",
        {"report": report}
    )