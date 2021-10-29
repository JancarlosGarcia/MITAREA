"""classroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from sistema_calificacion.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrar/', UsuarioNuevo.as_view(), name='register'),
    path('crear/curso', CreateCurso.as_view(), name='curso'),
    path('crear/rol', CreateRol.as_view(), name='rol'),
    path('accounts/profile/', perfil, name='perfil'),
    path('tabla/<int:pk>', TableCalifications.as_view(),name='tabla'),
    path('crear/tareaa/<int:pk>',ViewCrearTarea.as_view(),name='crearTarea'),
    path('home/', HomeLogin.as_view(), name='inicio'),
    path('subir/tarea/<int:pk>', ViewSubirTarea.as_view(),name='subir'),
    path('asignar/rol/<int:pk>', AsignarRol.as_view(), name='crearrol'),
    path('', home, name='home'),
    path('calificar/tarea/<int:pk>',ViewCalificarTarea.as_view(),name='calificar'),
    path('asingar/', CreateAsignacion.as_view(), name='asignarCurso'),
    path('registrar/asignacion', RegistrarAsignacion.as_view(),name='asignacion'),
    path('listaTareas/<int:pk>',ListaTareas.as_view(),name='lista'),
    path('403/',prohibido,name='403'),
    path('listar/estudiantesCurso/<int:pk>',ListStudentsCourse.as_view(),name='asignados'),
    path('listar/estudiantes', ListStudent.as_view(), name='estudiantes'),
    path('accounts/', include('django.contrib.auth.urls'))
]
