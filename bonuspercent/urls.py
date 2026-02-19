from django.urls import path
from .views import index, bonus_report, supplier_list_sorted, supplier_edit, supplier_delete, purchase_list_sorted, purchase_edit, purchase_delete

app_name = "bonuspercent"

urlpatterns = [
    path("", index, name="index"), # форми за попълванв
    path("report/", bonus_report, name="bonus_report"), # отчет за % бонус
    path("suppliers/", supplier_list_sorted, name="supplier_list_sorted"), # списък с доставки за проверка на редакция
    path("suppliers/edit/<int:pk>/", supplier_edit, name="supplier_edit"),
    path("suppliers/delete/<int:pk>/", supplier_delete, name="supplier_delete"),
    path("purchases/", purchase_list_sorted, name="purchase_list_sorted"), # списък с покупки за проверка на редакция
    path("purchases/edit/<int:pk>/", purchase_edit, name="purchase_edit"),
    path("purchases/delete/<int:pk>/", purchase_delete, name="purchase_delete"),
]