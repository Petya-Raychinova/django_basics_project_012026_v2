from django import forms
from .models import PromoConditionsPercent, SalesQTY


class ConditionPromoForm(forms.ModelForm):
    class Meta:
        model = PromoConditionsPercent
        fields = [
            "product_id",
            "product_name",
            "purchasing_price",
            "percent_discount",
        ]

class SalesForm(forms.ModelForm):
    class Meta:
        model = SalesQTY
        fields = [
            "product_id",
            "sold_qty",
        ]