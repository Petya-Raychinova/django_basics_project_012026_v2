from django import forms
from .models import ConditionsPercent, PurchasingAmount

#forms.ModelForm - реферира към структурата на модела, когато формата има модел за по- кратко писане
#Search формата няма модел и се приви с forms.Form

class ConditionForm(forms.ModelForm):
    class Meta:
        model = ConditionsPercent
        fields = [
            "eik",
            "supplier_name",
            "percent_condition",
        ]


class PurchasingForm(forms.ModelForm):
    class Meta:
        model = PurchasingAmount
        fields = [
            "eik",
            "purchasing_amount",
        ]
