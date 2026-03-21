from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
import os
from .forms import ContractUploadForm, ContractDocument


def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ContractUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,
            "Договорът е успешно качен в архива.",
            extra_tags="contract")
            return redirect("contract_documents:index")

    else:
        form = ContractUploadForm()

    return render(request, "contract_documents/index.html", {"form": form})

def contract_list(request: HttpRequest) -> HttpResponse:
    contracts = ContractDocument.objects.select_related("supplier").order_by("-uploaded_at")

    return render(
        request,
        "contract_documents/contract_list.html",
        {"contracts": contracts},
    )

def delete_contract(request, pk):
    contract = get_object_or_404(ContractDocument, pk=pk)

    if request.method == "POST":
        if contract.document:
            if os.path.isfile(contract.document.path):
                os.remove(contract.document.path)

        contract.delete()

        messages.success(
            request,
            "Договорът е изтрит успешно.",
            extra_tags="contract"
        )

        return redirect("contract_documents:list")

    return redirect("contract_documents:list")

def edit_contract(request, pk):
    contract = get_object_or_404(ContractDocument, pk=pk)

    if request.method == "POST":
        form = ContractUploadForm(request.POST, request.FILES, instance=contract)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Договорът е редактиран успешно.",
                extra_tags="contract"
            )

            return redirect("contract_documents:list")
    else:
        form = ContractUploadForm(instance=contract)

    return render(
        request,
        "contract_documents/edit_contract.html",
        {"form": form, "contract": contract},
    )