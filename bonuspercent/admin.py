from django.contrib import admin
from .models import ConditionsPercent
from .models import PurchasingAmount

@admin.register(ConditionsPercent)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('eik', 'supplier_name', 'percent_condition')
    search_fields = ('eik', 'supplier_name')

@admin.register(PurchasingAmount)
class PurchasingAdmin(admin.ModelAdmin):
    list_display = ('get_eik', 'purchasing_amount')

    def get_eik(self, obj):
        return obj.condition.eik

    get_eik.short_description = 'eik'