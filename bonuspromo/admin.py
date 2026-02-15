from django.contrib import admin

from bonuspromo.models import PromoConditionsPercent, SalesQTY


@admin.register(PromoConditionsPercent)
class PromoConditionsAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'purchasing_price', 'percent_discount')
    search_fields = ('product_id', 'product_name')

@admin.register(SalesQTY)
class QtyPromoAdmin(admin.ModelAdmin):
    list_display = ('get_product_id', 'sold_qty')

    def get_product_id(self, obj):
        return obj.condition.product_id

    get_product_id.short_description = 'product_id'
