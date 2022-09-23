from django import forms
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class FormularioMensaje(forms.Form):

    nombre=forms.CharField(max_length=30)
    apellido=forms.CharField(max_length=30)
    destinatario=forms.CharField(max_length=60)
    email=forms.EmailField(max_length=50)
    mensaje=RichTextField()
    fecha=forms.DateField()