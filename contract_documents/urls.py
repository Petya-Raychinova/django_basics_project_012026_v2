from django.urls import path
from . import views

app_name = "contract_documents"

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.contract_list, name="list"),
    path("delete/<int:pk>/", views.delete_contract, name="delete"),
    path("edit/<int:pk>/", views.edit_contract, name="edit"),
]