from http.client import HTTPResponse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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

def promo_report(request: HttpRequest) -> HttpResponse:

    products = (
        PromoConditionsPercent.objects
        .annotate(total_qty=Sum("salesqty__sold_qty"))
    )

    report_qty = []

    for p in products:
        total_qty = p.total_qty or 0

        promo_bonus = (
            total_qty *
            p.purchasing_price *
            p.percent_discount / 100
        )

        report_qty.append({
            "product_id": p.product_id,
            "product_name": p.product_name,
            "purchasing_price": p.purchasing_price,
            "percent_discount": p.percent_discount,
            "total_qty": total_qty,
            "promo_bonus": promo_bonus,
        })

    return render(
        request,
        "bonuspromo/bonus_promo_report.html",
        {"report_qty": report_qty}
    )

def promo_conditions_list_sorted(request):
    promos = PromoConditionsPercent.objects.all()

    return render(
        request,
        "bonuspromo/promo_conditions_list_sorted.html",
        {"promos": promos}
    )

def promo_conditions_edit(request, pk):
    promo = get_object_or_404(PromoConditionsPercent, pk=pk)

    if request.method == "POST":
        form = ConditionPromoForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            return redirect("bonuspromo:promo_conditions_list_sorted")
    else:
        form = ConditionPromoForm(instance=promo)

    return render(
        request,
        "bonuspromo/promo_conditions_edit.html",
        {"form": form}
    )

def promo_conditions_delete(request, pk):
    promo = get_object_or_404(PromoConditionsPercent, pk=pk)

    if request.method == "POST":
        promo.delete()
        return redirect("bonuspromo:promo_conditions_list_sorted")

    return render(
        request,
        "bonuspromo/promo_conditions_delete.html",
        {"promo": promo}
    )


from django.shortcuts import render, redirect, get_object_or_404
from .models import SalesQTY
from .forms import SalesForm



def sales_qty_list_sorted(request):
    sales = (
        SalesQTY.objects
        .select_related("product_id")
        .order_by("product_id__product_id")
    )

    return render(
        request,
        "bonuspromo/sales_qty_list_sorted.html",
        {"sales": sales}
    )


def sales_qty_edit(request, pk):
    sale = get_object_or_404(SalesQTY, pk=pk)

    if request.method == "POST":
        form = SalesForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect("bonuspromo:sales_list")
    else:
        form = SalesForm(instance=sale)

    return render(
        request,
        "bonuspromo/sales_qty_edit.html",
        {"form": form}
    )


def sales_qty_delete(request, pk):
    sale = get_object_or_404(SalesQTY, pk=pk)

    if request.method == "POST":
        sale.delete()
        return redirect("bonuspromo:sales_list")

    return render(
        request,
        "bonuspromo/sales_qty_delete.html",
        {"sale": sale}
    )
