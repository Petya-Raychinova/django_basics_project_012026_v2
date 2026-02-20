from django import forms
from django.core.exceptions import ValidationError

from .models import ConditionsPercent, PurchasingAmount


class ConditionForm(forms.ModelForm):

    class Meta:
        model = ConditionsPercent
        fields = "__all__"
        widgets = {
            "eik": forms.TextInput(attrs={
                "placeholder": "EIK (10-13 цифри)"
            }),
            "supplier_name": forms.TextInput(attrs={
                "placeholder": "Кирилица или латиница"
            }),
            "percent_bonus": forms.NumberInput(attrs={
                "placeholder": "От 0 до 100"
            }),
            "categories": forms.CheckboxSelectMultiple(),
        }
        error_messages = {
            "eik": {
                "unique": "Вече съществува доставчик с този EIK."
            }
        }

    def clean_eik(self):
        eik = self.cleaned_data.get("eik", "").strip()

        # Проверка дали съдържа само цифри
        if not eik.isdigit():
            raise ValidationError(
                "EIK трябва да съдържа само цифри."
            )

        # Проверка дали е точно 9 цифри
        if not (10 <= len(eik) <= 13):
            raise ValidationError(
                "EIK трябва да съдържа между 10 и 13 цифри."
            )

        # Проверка за дублиране
        qs = ConditionsPercent.objects.filter(eik=eik)

        # Ако редактираме запис – да не брои самия него
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(
                "Вече съществува доставчик с този EIK."
            )

        return eik

    def clean_supplier_name(self):
        supplier_name = self.cleaned_data.get("supplier_name", "").strip()

        # Проверка дали съдържа само букви (кирилица и латиница)
        if not supplier_name.replace(" ", "").isalpha():
            raise ValidationError(
                "Името на доставчика може да съдържа само букви на кирилица и/или латиница."
            )

        return supplier_name

    def clean_percent_condition(self):
        percent = self.cleaned_data.get("percent_condition")

        if percent is None:
            return percent

        if percent < 0:
            raise ValidationError(
                "Процентът не може да бъде отрицателно число."
            )

        if percent > 100:
            raise ValidationError(
                "Процентът не може да бъде по-голям от 100."
            )

        return percent

class PurchasingForm(forms.ModelForm):

    class Meta:
        model = PurchasingAmount
        fields = [
            "condition_eik",
            "purchasing_amount",
        ]
        widgets = {
            "purchasing_amount": forms.TextInput(attrs={
                "placeholder": "Максимум 15 цифри"
            })
        }