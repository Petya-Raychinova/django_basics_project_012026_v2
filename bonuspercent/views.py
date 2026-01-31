from django.forms import DecimalField
from django.shortcuts import render, redirect
from .forms import ConditionForm, PurchasingForm
from .models import ConditionsPercent, PurchasingAmount
from django.db.models import Sum, ExpressionWrapper, F

# създава форма за попълване, валидира входа и записва в базата

def index(request):
    condition_form = ConditionForm()
    purchasing_form = PurchasingForm()

    if request.method == "POST":
        if "add_condition" in request.POST:
            condition_form = ConditionForm(request.POST)
            if condition_form.is_valid():
                condition_form.save()
                return redirect("index")

        elif "add_purchase" in request.POST:
            purchasing_form = PurchasingForm(request.POST)
            if purchasing_form.is_valid():
                eik = purchasing_form.cleaned_data["EIK"]
                amount = purchasing_form.cleaned_data["purchasing_amount"]

                condition = ConditionsPercent.objects.get(EIK=eik)
                PurchasingAmount.objects.create(
                    condition=condition,
                    purchasing_amount=amount
                )
                return redirect("index")

    return render(
        request,
        "bonus_percent/index.html",
        {
            "condition_form": condition_form,
            "purchasing_form": purchasing_form,
        }
    )

# калкулация на самия бонус

def bonus_report(request):
    report = (
        PurchasingAmount.objects
        .select_related("condition")
        .values(
            "condition__EIK",
            "condition__supplier_name",
            "condition__percent_condition",
        )
        .annotate(
            total_amount=Sum("purchasing_amount"),
            bonus=ExpressionWrapper(
                Sum("purchasing_amount") * F("condition__percent_condition") / 100,
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
    )

    return render(
        request,
        "bonus_percent/bonus_report.html",
        {"report": report}
    )