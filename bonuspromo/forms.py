from django import forms
from django.core.exceptions import ValidationError
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
        widgets = {
            "product_id": forms.TextInput(attrs={
                "placeholder": "Точно 9 цифри"
            }),
            "product_name": forms.TextInput(attrs={
                "placeholder": "Кирилица или латиница"
            }),
            "purchasing_price": forms.NumberInput(attrs={
                "placeholder": "Максимум 4 цифри",
                "step": "0.01",
                "min": "0"
            }),
            "percent_discount": forms.NumberInput(attrs={
                "placeholder": "От 0 до 100"
            }),
        }

        error_messages = {
            "product_id": {
                "unique": "Вече съществува продукт с този ID."
            }
        }

    def clean_product_name(self):
        product_name = self.cleaned_data.get("product_name", "").strip()

        # Позволява само букви (кирилица и латиница)
        pattern = r'^[A-Za-zА-Яа-яЁё]+$'

        if not product_name.replace(" ", "").isalpha():
            raise ValidationError(
                "Името на продукта може да съдържа само букви на кирилица или латиница."
            )

        return product_name

    def clean_percent_discount(self):
        percent = self.cleaned_data.get("percent_discount")

        if percent is None:
            return percent

        if percent < 0:
            raise ValidationError(
                "Процентът не може да бъде отрицателен."
            )

        if percent > 100:
            raise ValidationError(
                "Процентът не може да бъде по-голям от 100."
            )

        return percent

    def clean_product_id(self):
        product_id = self.cleaned_data["product_id"]

        #маха интервали
        product_id = product_id.strip()

        #дали е точно 9 символа
        if len(product_id) != 9:
            raise forms.ValidationError(
                "ID на продукта трябва да съдържа точно 9 цифри."
            )

        # дали са само цифри
        if not product_id.isdigit():
            raise forms.ValidationError(
                "ID на продукта трябва да съдържа само цифри."
            )

        return product_id



class SalesForm(forms.ModelForm):
    class Meta:
        model = SalesQTY
        fields = [
            "product_id",
            "sold_qty",
        ]
        widgets = {
            "sold_qty": forms.TextInput(attrs={
                "placeholder": "Максимум 10 цифри"
            })
        }