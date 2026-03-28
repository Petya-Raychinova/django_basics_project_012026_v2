from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from .views import nav

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", nav, name="nav"), #стартова страница, от която ще се навигира
    path('bonuspercent/', include('bonuspercent.urls')),
    path('bonuspromo/', include('bonuspromo.urls')),
    path("import/", include("import_purchasing_amount.urls")),
    path("import_promo/", include("import_promo_qty.urls")),
    path("contracts/", include("contract_documents.urls")),
    path("accounts/", include("accounts.urls")),
    path('', include('bonuspercent.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def custom_404(request, exception):
    return render(request, "404.html", status=404)

handler404 = "djangobasicsproject.urls.custom_404"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)