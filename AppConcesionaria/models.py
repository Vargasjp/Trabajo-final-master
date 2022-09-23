from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Vehiculos(models.Model):
    marca=models.CharField(max_length=40)
    tipo=models.CharField(max_length=40)
    color=models.CharField(max_length=40)
    kilometros=models.IntegerField()
    imagen=models.ImageField(upload_to="imagenes", null=True)
    fechaDePublicacion=models.DateTimeField(default=datetime.datetime.now)
    
    def __str__(self):
        return self.marca+" "+str(self.tipo)

class Avatar(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to="avatares", null=True, blank=True)