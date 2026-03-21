from django import forms
from .models import ContractDocument


class ContractUploadForm(forms.ModelForm):
    class Meta:
        model = ContractDocument
        fields = ["supplier", "document", "description"]
        labels = {
            "supplier": "Избери доставчик",
            "document": "Избери документ за качване .pdf",
            "description": "Описание",
        }
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "placeholder": "Напр.: Анекс за бонус от 01.01.2026 г."
                }
            ),
        }