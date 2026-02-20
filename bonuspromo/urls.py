from django.urls import path
from .views import index, promo_report, promo_conditions_list_sorted, promo_conditions_edit, promo_conditions_delete, \
    sales_qty_list_sorted, sales_qty_edit, sales_qty_delete

app_name = "bonuspromo"

urlpatterns = [
    path("", index, name="index"), # форми за попълванв
    path("report/", promo_report, name="promo_report"), # отчет за промо отстъпка
    path("promo-list/", promo_conditions_list_sorted, name="promo_list"),
    path("promo-edit/<int:pk>/", promo_conditions_edit, name="promo_conditions_edit"),
    path("promo-delete/<int:pk>/", promo_conditions_delete, name="promo_conditions_delete"),
    path("sales-list/", sales_qty_list_sorted, name="sales_list"),
    path("sales-edit/<int:pk>/", sales_qty_edit, name="sales_qty_edit"),
    path("sales-delete/<int:pk>/", sales_qty_delete, name="sales_qty_delete"),

]