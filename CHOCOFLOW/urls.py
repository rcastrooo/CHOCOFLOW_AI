from django.urls import path
from myApp.views import index, registro, login_usuario

urlpatterns = [
    path('', index, name='index'),
     path('login/', login_usuario, name='login'),
    path('registro/', registro, name='registro'),
]