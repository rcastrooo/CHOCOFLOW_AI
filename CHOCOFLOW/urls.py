from django.contrib import admin
from django.urls import path
from myApp.views import index  # ✅ IMPORT CORRECTO

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
]