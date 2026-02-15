from django.urls import path
from .views import index, promo_report

app_name = "bonuspromo"

urlpatterns = [
    path("", index, name="index"), # форми за попълванв
    path("report/", promo_report, name="promo_report"), # отчет за промо отстъпка
]