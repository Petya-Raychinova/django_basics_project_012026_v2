from django import forms
from .models import ConditionsPercent, PurchasingAmount


class ConditionForm(forms.ModelForm):
    class Meta:
        model = ConditionsPercent
        fields = [
            "eik",
            "supplier_name",
            "percent_condition",
        ]

class PurchasingForm(forms.Form):
    eik = forms.CharField(
        max_length=13,
        label="ЕИК на доставчик"
    )
    purchasing_amount = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        label="Сума на покупка"
    )
