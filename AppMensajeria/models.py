from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
import datetime
# Create your models here.

class Mensaje(models.Model):
    fecha=models.DateField()
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    destinatario=models.ForeignKey(User, related_name="destinatario", on_delete=models.CASCADE)
    email=models.EmailField(max_length=50)
    mensaje=RichTextField()
    fecha=models.DateTimeField()