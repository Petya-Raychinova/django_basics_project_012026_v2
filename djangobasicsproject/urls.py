from django.contrib import admin
from django.urls import path, include
from .views import nav

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", nav, name="nav"), #стартова страница, от която ще се навигира
    path('bonuspercent/', include('bonuspercent.urls')),
    path('bonuspromo/', include('bonuspromo.urls')),
    path("import/", include("import_purchasing_amount.urls")),

]