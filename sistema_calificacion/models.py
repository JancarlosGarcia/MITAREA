from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator



class Roles(models.Model):
    id_rol = models.BigAutoField(primary_key=True, null=False, blank=False)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class UserApp(models.Model):
    id_userApp = models.OneToOneField(User, on_delete=models.CASCADE)
    rol_teacher = models.ForeignKey(Roles, on_delete=models.CASCADE, default=4)
    parent_email = models.EmailField()

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            UserApp.objects.create(id_userApp=instance)

    def __str__(self):
        return f'{self.id_userApp.first_name} {self.id_userApp.last_name}'


class Curso(models.Model):
    id_curso = models.BigAutoField(primary_key=True, null=False, blank=False)
    name_curso = models.CharField(max_length=50)
    teacher = models.ForeignKey(UserApp, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.name_curso


class Asignacion(models.Model):
    id_asignacion = models.BigAutoField(primary_key=True, null=False, blank=False)
    id_student = models.ForeignKey(UserApp, on_delete=models.CASCADE, default=0)
    year: int = datetime.now().year
    year = models.IntegerField(default=2021,validators=[
        MaxValueValidator(year+1),
        MinValueValidator(year)
    ])

    def __str__(self):
        return f'{self.id_student.id_userApp.first_name} {self.id_student.id_userApp.last_name}  Ciclo:{self.year}'


class CursoAsignacion(models.Model):
    id_curso_asignacion = models.BigAutoField(primary_key=True, null=False, blank=False)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, default=0)
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE, default=0)
    tareas = models.IntegerField(default=0,validators=[
        MaxValueValidator(30),
        MinValueValidator(0)
    ])
    primer_parcial = models.IntegerField(default=0,validators=[
        MaxValueValidator(10),
        MinValueValidator(0)
    ])
    segundo_parcial = models.IntegerField(default=0, validators=[
        MaxValueValidator(20),
        MinValueValidator(0)
    ])
    final = models.IntegerField(default=0, validators=[
        MaxValueValidator(40),
        MinValueValidator(0)
    ])
    total = models.IntegerField(default=0,validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])

    def save(self):
        self.total = self.tareas+self.primer_parcial+self.segundo_parcial+self.final
        return super(CursoAsignacion, self).save()

    def __str__(self):
        return self.curso.name_curso


class Bloque(models.Model):
    id_bloque = models.BigAutoField(primary_key=True, null=False, blank=False)
    curso_asignacion = models.ForeignKey(CursoAsignacion, on_delete=models.CASCADE, default=0)
    Parcial = models.IntegerField(default=0)
    total_bloque = models.IntegerField()


class Files(models.Model):
    id_file = models.BigAutoField(primary_key=True, null=False, blank=False)
    file = models.FileField(upload_to='./files')
    owner = models.ForeignKey(UserApp, on_delete=models.CASCADE)


class Tareas(models.Model):
    id_tarea = models.BigAutoField(primary_key=True,null=False, blank=False)
    title = models.CharField(max_length=50, null=False, blank=True)
    description = models.CharField(max_length=500, null=False, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, default=0)
    valor = models.IntegerField(default=0)
    fecha_de_entrega = models.DateTimeField()




    def __str__(self):
        return self.title


class EntregaTareas(models.Model):
    codigo_tarea = models.BigAutoField(primary_key=True)
    tarea = models.ForeignKey(Tareas, on_delete=models.CASCADE, default=1)
    alumno = models.ForeignKey(UserApp, on_delete=models.CASCADE, default=4)
    calificacion = models.IntegerField(default=0)
    archivo_asociado = models.FileField(upload_to='./tareas')
    fecha_de_subida = models.DateTimeField(null=True)

    def __str__(self):
        try:
            fecha = self.fecha_de_subida.strftime("%m/%d/%Y")
        except:
            fecha = '0'
        return f'{self.alumno.id_userApp.first_name} {self.alumno.id_userApp.last_name}  {fecha}'


