from django import forms

class UploadPurchasingAmount(forms.Form):
    upload_file = forms.FileField()
