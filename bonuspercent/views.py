from http.client import HTTPResponse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum

from .forms import ConditionForm, PurchasingForm
from .models import ConditionsPercent, PurchasingAmount
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import ConditionsPercent


def index(request: HttpRequest) -> HTTPResponse:
    condition_form = ConditionForm()
    purchasing_form = PurchasingForm()

    if request.method == "POST":
        if "add_condition" in request.POST:
            condition_form = ConditionForm(request.POST)
            if condition_form.is_valid():
                condition = condition_form.save()
                messages.success(request, f"Доставчикът за % бонус е добавен успешно. ID: {condition.id}",extra_tags="supplier")

                return redirect("bonuspercent:index")

        elif "add_purchase" in request.POST:
            purchasing_form = PurchasingForm(request.POST)
            if purchasing_form.is_valid():
                purchase = purchasing_form.save()
                messages.success(request, f"Покупката към доставчика е добавена успешно.  ID: {purchase.id}",extra_tags="purchase")
                return redirect("bonuspercent:index")

    return render(
        request,
        "bonuspercent\index.html",
        {
            "condition_form": condition_form,
            "purchasing_form": purchasing_form
        }
    )

def bonus_report(request: HttpRequest) -> HttpResponse:
    purchases = (
        PurchasingAmount.objects
        .values(
            "condition_eik__eik",
            "condition_eik__supplier_name",
            "condition_eik__percent_condition"
        )
        .annotate(total_amount=Sum("purchasing_amount"))
    )

    report = []

    for p in purchases:
        bonus = p["total_amount"] * p["condition_eik__percent_condition"] / 100

        report.append({
            "eik": p["condition_eik__eik"],
            "supplier_name": p["condition_eik__supplier_name"],
            "percent_condition": p["condition_eik__percent_condition"],
            "total_amount": p["total_amount"],
            "bonus": bonus,
        })

    return render(
        request,
        "bonuspercent/bonus_report.html",
        {"report": report}
    )

def supplier_list_sorted(request):
    suppliers = ConditionsPercent.objects.all().order_by("eik")

    return render(
        request,
        "bonuspercent/supplier_list_sorted.html",
        {"suppliers": suppliers}
    )

def supplier_edit(request, pk):
    supplier = get_object_or_404(ConditionsPercent, pk=pk)

    if request.method == "POST":
        form = ConditionForm(request.POST, instance=supplier)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Доставчик ID {supplier.id} е редактиран успешно.",
                extra_tags="supplier"
            )
            return redirect("bonuspercent:supplier_list_sorted")
    else:
        form = ConditionForm(instance=supplier)

    return render(
        request,
        "bonuspercent/supplier_edit.html",
        {"form": form, "supplier": supplier}
    )


def supplier_delete(request, pk):
    supplier = get_object_or_404(ConditionsPercent, pk=pk)

    if request.method == "POST":
        supplier.delete()

        messages.success(
            request,
            f"Доставчикът (ID: {pk}) беше изтрит успешно.",
            extra_tags="supplier"
        )

        return redirect("bonuspercent:supplier_list_sorted")

    return render(
        request,
        "bonuspercent/supplier_confirm_delete.html",
        {"supplier": supplier}
    )


def purchase_list_sorted(request):
    purchases = PurchasingAmount.objects.select_related("condition_eik").all().order_by("id")

    return render(
        request,
        "bonuspercent/purchase_list_sorted.html",
        {"purchases": purchases}
    )

def purchase_edit(request, pk):
    purchase = get_object_or_404(PurchasingAmount, pk=pk)

    if request.method == "POST":
        form = PurchasingForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            messages.success(request, "Покупката е редактирана успешно.")
            return redirect("bonuspercent:purchase_list_sorted")
    else:
        form = PurchasingForm(instance=purchase)

    return render(
        request,
        "bonuspercent/purchase_edit.html",
        {"form": form}
    )


def purchase_delete(request, pk):
    purchase = get_object_or_404(PurchasingAmount, pk=pk)

    if request.method == "POST":
        purchase.delete()
        messages.success(request, "Покупката е изтрита успешно.")
        return redirect("bonuspercent:purchase_list_sorted")

    return render(
        request,
        "bonuspercent/purchase_confirm_delete.html",
        {"purchase": purchase}
    )
