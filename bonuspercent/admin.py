from django.contrib import admin
from .models import ConditionsPercent, PurchasingAmount, ProductCategory

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

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('product_category_name',)


