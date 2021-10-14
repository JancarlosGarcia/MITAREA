from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User, AbstractUser



class Roles(models.Model):
    id_rol = models.BigAutoField(primary_key=True, null=False, blank=False)
    description = models.CharField(max_length=50)

class UserApp(models.Model):
    id_userApp = models.OneToOneField(User, on_delete=models.CASCADE)
    rol_teacher = models.ForeignKey(Roles, on_delete=models.CASCADE, default=1)
    parent_email = models.EmailField()

    def __str__(self):
        return self.id_userApp.username

class Curso(models.Model):
    id_curso = models.BigAutoField(primary_key=True, null=False, blank=False)
    name_curso = models.CharField(max_length=50)
    teacher = models.ForeignKey(UserApp, on_delete=models.CASCADE, default=0)

class Asignacion(models.Model):
    id_asignacion = models.BigAutoField(primary_key=True, null=False, blank=False)
    id_student = models.ForeignKey(UserApp, on_delete=models.CASCADE, default=0)
    year = models.IntegerField()

class CursoAsignacion(models.Model):
    id_curso_asignacion = models.BigAutoField(primary_key=True, null=False, blank=False)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, default=0)
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE, default=0)
    total = models.IntegerField()


class Bloque(models.Model):
    id_bloque = models.BigAutoField(primary_key=True, null=False, blank=False)
    curso_asignacion= models.ForeignKey(CursoAsignacion,on_delete=models.CASCADE,default=0)
    total_bloque = models.IntegerField()


class Files(models.Model):
    id_file = models.BigAutoField(primary_key=True, null=False, blank=False)
    file = models.FileField(upload_to='./files')
    owner = models.ForeignKey(UserApp, on_delete=models.CASCADE)






