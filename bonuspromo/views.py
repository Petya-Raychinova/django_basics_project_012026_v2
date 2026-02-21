from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages

from .forms import ConditionPromoForm, SalesForm
from .models import PromoConditionsPercent, SalesQTY

def index(request: HttpRequest) -> HttpResponse:
    condition_promo_form = ConditionPromoForm()
    sales_form = SalesForm()

    if request.method == "POST":

        # добавя условие
        if "add_promo_condition" in request.POST:
            condition_promo_form = ConditionPromoForm(request.POST)

            if condition_promo_form.is_valid():
                promo = condition_promo_form.save()

                messages.success(
                    request,
                    f"Промо продуктът е добавен успешно. ID: {promo.id}",
                    extra_tags="promo"
                )

                return redirect("bonuspromo:index")

        # добавяме продажба
        elif "add_sold_qty" in request.POST:
            sales_form = SalesForm(request.POST)

            if sales_form.is_valid():
                sale = sales_form.save()

                messages.success(
                    request,
                    f"Продажбата е добавена успешно. ID: {sale.id}",
                    extra_tags="sales"
                )

                return redirect("bonuspromo:index")

    return render(
        request,
        "bonuspromo/index.html",
        {
            "condition_promo_form": condition_promo_form,
            "sales_form": sales_form
        }
    )

#отчет за промоциите
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
    promos = PromoConditionsPercent.objects.all().order_by("product_id")

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

            messages.success(
                request,
                f"Промо условието (ID: {promo.id}) е редактирано успешно.",
                extra_tags="promo"
            )

            return redirect("bonuspromo:promo_list")

    else:
        form = ConditionPromoForm(instance=promo)

    return render(
        request,
        "bonuspromo/promo_conditions_edit.html",
        {"form": form, "promo": promo}
    )


def promo_conditions_delete(request, pk):
    promo = get_object_or_404(PromoConditionsPercent, pk=pk)

    if request.method == "POST":
        promo.delete()

        messages.success(
            request,
            f"Промо условието (ID: {pk}) беше изтрито успешно.",
            extra_tags="promo"
        )

        return redirect("bonuspromo:promo_list")

    return render(
        request,
        "bonuspromo/promo_conditions_delete.html",
        {"promo": promo}
    )


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

            messages.success(
                request,
                f"Продажбата (ID: {sale.id}) е редактирана успешно.",
                extra_tags="sales"
            )

            return redirect("bonuspromo:sales_list")

    else:
        form = SalesForm(instance=sale)

    return render(
        request,
        "bonuspromo/sales_qty_edit.html",
        {"form": form, "sale": sale}
    )


def sales_qty_delete(request, pk):
    sale = get_object_or_404(SalesQTY, pk=pk)

    if request.method == "POST":
        sale.delete()

        messages.success(
            request,
            f"Продажбата (ID: {pk}) беше изтрита успешно.",
            extra_tags="sales"
        )

        return redirect("bonuspromo:sales_list")

    return render(
        request,
        "bonuspromo/sales_qty_delete.html",
        {"sale": sale}
    )
