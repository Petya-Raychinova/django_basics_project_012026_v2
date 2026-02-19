from django import forms
from django.core.exceptions import ValidationError

from .models import ConditionsPercent, PurchasingAmount, ProductCategory


#forms.ModelForm - реферира към структурата на модела, когато формата има модел за по- кратко писане
#Search формата няма модел и се приви с forms.Form

class ConditionForm(forms.ModelForm):
    class Meta:
        model = ConditionsPercent
        fields = "__all__"

    def clean_eik(self):
        eik = self.cleaned_data["eik"]

        qs = ConditionsPercent.objects.filter(eik=eik)

        # Ако редактираме съществуващ запис да не дава грешка, че съществъва вече този ЕИК
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Вече съществува доставчик с този ЕИК."
            )

        return eik


class PurchasingForm(forms.ModelForm):
    class Meta:
        model = PurchasingAmount
        fields = [
            "condition_eik",
            "purchasing_amount",
        ]


class ConditionForm(forms.ModelForm):

    categories = forms.ModelMultipleChoiceField(
        queryset=ProductCategory.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = ConditionsPercent
        fields = "__all__"