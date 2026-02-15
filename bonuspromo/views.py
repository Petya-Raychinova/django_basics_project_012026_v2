from http.client import HTTPResponse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.shortcuts import render

from .forms import ConditionPromoForm, SalesForm
from .models import PromoConditionsPercent, SalesQTY

def index (request: HttpRequest) -> HTTPResponse:
    condition_promo_form = ConditionPromoForm()
    sales_form = SalesForm()

    if request.method == "POST":
        if "add_promo_condition" in request.POST:
            condition_promo_form = ConditionPromoForm(request.POST)
            if condition_promo_form.is_valid():
                condition_promo_form.save()
                return redirect("bonuspromo:index")

        elif "add_sold_qty" in request.POST:
            sales_form =SalesForm(request.POST)
            if sales_form.is_valid():
                product_id = sales_form.cleaned_data["product_id"]
                qty = sales_form.cleaned_data["sold_qty"]

                SalesQTY.objects.create(
                    product_id=product_id,
                    sold_qty = qty
                )

                return redirect("bonuspromo:index")

    return render(
        request,
        "bonuspromo\index.html",
        {
            "condition_promo_form": condition_promo_form,
            "sales_form": sales_form
        }
    )

def promo_report(request: HttpRequest) -> HTTPResponse:
    qtys = (
        SalesQTY.objects
        .values("product_id")
        .annotate(total_qty = Sum("sold_qty"))
    )

    report_qty = []
    for q in qtys:
        condition_promo = PromoConditionsPercent.objects.filter(product_id=q["product_id"]).first()

        if not condition_promo:
            continue

        promo_bonus = q["total_qty"] * condition_promo.percent_discount/100
        report_qty.append({
            "product_id": q["product_id"],
            "product_name": condition_promo.product_name,
            "purchasing_price": condition_promo.purchasing_price,
            "percent_discount": condition_promo.percent_discount,
            "total_qty": q["total_qty"],
            "promo_bonus": promo_bonus,
        }
       )

    return render(
        request,
        "bonuspromo/bonus_promo_report.html",
        {"report_qty": report_qty}
    )