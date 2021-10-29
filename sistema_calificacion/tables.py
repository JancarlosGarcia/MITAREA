import django_tables2 as tables
from django_tables2.utils import A
from .models import CursoAsignacion

class TableButton(tables.Table):
    Editar = tables.LinkColumn("Editar", text='editar', args=[A("pk")])

    class Meta:
        model = CursoAsignacion
