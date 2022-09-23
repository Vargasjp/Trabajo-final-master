from django.http import HttpResponse
from http.client import HTTPResponse
from django.shortcuts import render

from AppConcesionaria.forms import *
from .models import Vehiculos, Avatar
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def inicio(request):
    return render(request, "AppConcesionaria/inicio.html")
    
def sobreNosotros(request):
    return render(request, "AppConcesionaria/sobreNosotros.html")
    
#Nuestros vehiculos-------------
@login_required
def vehiculosformulario(request):
    if request.method=="POST":
        Vehiform=VehiculoFormulario(request.POST, files=request.FILES)
        if Vehiform.is_valid():
            print(Vehiform)
            info=Vehiform.cleaned_data
            vehiculo=Vehiculos(marca=info["marca"],tipo=info["tipo"],color=info["color"],kilometros=info["kilometros"],imagen=info["imagen"])
            vehiculo.save()
            return render(request, "AppConcesionaria/inicio.html", {"mensaje": "Vehiculo Agregado"})
        else:
            return render(request, "AppConcesionaria/inicio.html", {"mensaje": "Error"})
    else:
        Vehiform=VehiculoFormulario()
        return render(request, "AppConcesionaria/accesoVehiculos.html", {"formulario":Vehiform})


def busquedaVehiculo(request):
    return render(request, "AppConcesionaria/busquedaVehiculo.html")

def buscar(request):
    if request.GET["marca"]:
        marca=request.GET["marca"]
        Marca=Vehiculos.objects.filter(marca=marca)
        if len(Marca)!=0:
            return render(request, "AppConcesionaria/ResultadoBusqueda.html", {"vehiculo":Marca})
        else:
            return render(request, "AppConcesionaria/ResultadoBusqueda.html", {"mensaje": "No hay vehiculos de esa Marca"})
    else:
        return render(request, "AppConcesionaria/busquedaVehiculo.html", {"mensaje": "No enviaste datos!"})



def leerVehiculos(request):
    vehiculos=Vehiculos.objects.all()
    contexto={"vehiculos":vehiculos}
    return render(request, "AppConcesionaria/nuestrosVehiculos.html", contexto)

@login_required
def editarVehiculo(request,id):
    vehi=Vehiculos.objects.get(id=id)
    if request.method=="POST":
        form=VehiculoFormulario(request.POST, request.FILES)
        if form.is_valid():
            info=form.cleaned_data
            vehi.marca=info["marca"]
            vehi.tipo=info["tipo"]
            vehi.color=info["color"]
            vehi.imagen=info["imagen"]
            vehi.kilometros=info["kilometros"]            
            vehi.save()            
        return render(request, "AppConcesionaria/guardado.html", {"Vehiculo":vehi})
    else:
        form=VehiculoFormulario(initial={"marca":vehi.marca, "tipo":vehi.tipo, "color":vehi.color, "kilometros":vehi.kilometros, "imagen":vehi.imagen })
        return render(request, "AppConcesionaria/editarVehiculo.html", {"formulario":form, "marca":vehi.marca, "id":vehi.id})


def verMas(request,id):
    vehi=Vehiculos.objects.get(id=id)
    imagen=vehi.imagen
    return render(request, "AppConcesionaria/verMas.html", { "vehiculo":vehi, "imagen":imagen})

@login_required
def eliminarVehiculo(request, id):
    Vehi=Vehiculos.objects.get(id=id)
    Vehi.delete()
    vehiculos=Vehiculos.objects.all()
    return render(request, "AppConcesionaria/nuestrosVehiculos.html", {"vehiculos":vehiculos})

#usuario
def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usu=form.cleaned_data.get("username")
            clave=form.cleaned_data.get("password")
            usuario=authenticate(username=usu, password=clave)
            if usuario is not None:
                login(request, usuario)
                return render(request, "AppConcesionaria/inicio.html", {"mensaje":f"Bienvenido {usuario}"})
            else:
                return render(request, "AppConcesionaria/login.html", {"form":form,"mensaje":"Usuario o contraseña incorrectos"})
        else:
            return render(request, "AppConcesionaria/login.html", {"form":form,"mensaje":"Formulario Invalido"})
    else:
        form=AuthenticationForm()
        return render(request, "AppConcesionaria/login.html", {"form":form})

def register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            form.save()
            return render(request, "AppConcesionaria/inicio.html", {"mensaje":f"Usuario: {username} creado"})
    else:
        form=UserRegisterForm()
    return render(request,"AppConcesionaria/register.html", {"form":form})

@login_required
def editarPerfil(request):
    usuario=request.user
    if request.method=="POST":
        form=UserEditform(request.POST, instance=usuario)
        if form.is_valid():
            usuario.first_name=form.cleaned_data["first_name"]
            usuario.last_name=form.cleaned_data["last_name"]
            usuario.email=form.cleaned_data["email"]
            usuario.save()
            return render(request, "AppConcesionaria/inicio.html", {"mensaje":f"Perfil de {usuario} editado"})
    else:
        form=UserEditform(instance=usuario)
        return render(request, "AppConcesionaria/editarPerfil.html", {"form":form, "usuario":usuario})

def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
        imagen=lista[0].imagen.url
    else:
        imagen=None
    return imagen

def agregarAvatar(request):
    if request.method=="POST":
        formulario=AvatarForm(request.POST, request.FILES)
        if formulario.is_valid():
            avatarViejo=Avatar.objects.filter(user=request.user)
            if (len(avatarViejo)>0):
                avatarViejo.delete()
            avatar=Avatar(user=request.user , imagen=formulario.cleaned_data["imagen"])
            avatar.save()
            return render(request, "AppCoder/inicio.html", {"usuario":request.user, "mensaje":"AVATAR AGREGADO EXITOSAMENTE","imagen":obtenerAvatar(request)})
    else:
        formulario=AvatarForm()
    return render(request, "AppCoder/agregarAvatar.html", {"form":formulario, "usuario":request.user,"imagen":obtenerAvatar(request)})

