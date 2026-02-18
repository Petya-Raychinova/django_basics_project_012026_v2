from django.urls import path
from . import views

app_name = "import_purchasing_amount"

urlpatterns = [
    path('', views.index, name='index'),
]
