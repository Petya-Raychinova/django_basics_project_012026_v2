from django import forms

class UploadSalesQTY(forms.Form):
    upload_file_promo_qty = forms.FileField()
