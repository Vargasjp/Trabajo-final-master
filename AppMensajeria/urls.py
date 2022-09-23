from django.urls import path
from AppMensajeria.views import *

urlpatterns = [
    path("crearMensaje/", CrearMensaje.as_view(), name="crearMensaje"),
    path("leerMensajes/", leerMensajes, name="leerMensajes"),
    path("verMensaje/<id>", verMensaje, name="verMensaje"),
]