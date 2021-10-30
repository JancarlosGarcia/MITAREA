import django_tables2 as tables
from django_tables2.utils import A
from .models import CursoAsignacion,UserApp

class TableButton(tables.Table):
    Editar = tables.LinkColumn("editar", text='editar', args=[A("pk"), A('curso.id_curso')])
    entregas = tables.LinkColumn('entregasAlumno', text='Entregas por alumnos', args=[A("asignacion.id_student.id"),
                                                                                      A("curso.id_curso")])

    class Meta:
        model = CursoAsignacion

class EstablecerEmail(tables.Table):
    Editar = tables.LinkColumn("updaterol", text="editar rol y correo", args=[A("pk")])
    Editar_perfil = tables.LinkColumn("editarperfil",text="editar perfil",args=[A("id_userApp.id")])

    class Meta:
        model = UserApp
