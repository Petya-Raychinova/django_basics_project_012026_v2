from django.shortcuts import render

def nav(request):
    return render(request, "nav.html")