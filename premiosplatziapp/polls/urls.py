from django.urls import path
from . import views                 #Desde la carpeta actual, que es un paquete, importar las vistas

urlpatterns = [
    path("", views.index, name="index"),
]