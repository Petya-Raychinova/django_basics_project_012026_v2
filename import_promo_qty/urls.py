from django.urls import path
from . import views

app_name = "import_promo_qty"

urlpatterns = [
    path('', views.index, name='index'),
]
