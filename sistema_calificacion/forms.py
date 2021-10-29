from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.contrib.auth.models import User


class FormUser(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(FormUser, self).__init__(*args, **kwargs)
        dict_label: dict = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo',
            'password1': 'Contraseña',
            'password2': 'Repita contraseña'
        }
        dict_help_text: dict = {
            'username': '<ul><li>Campo requerido maximo de 150 caracteres</li>'
                        '<li>Maximo 150 caracteres</li>'
                        '<li>Se permiter unicamente numeros ,letras y algunos caracteres</li></ul>',
            'password1': 'Debe llevar mas de 8 caracteres',
            'password2': 'Repita la contraseña'
        }
        for key in dict_label:
            current_field = self.fields[key]
            current_field.widget.attrs['class'] = 'form-control'
            current_field.label = dict_label[key]
            if key in dict_help_text:
                current_field.help_text = dict_help_text[key]


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('id_curso', 'name_curso', 'teacher')

    def __init__(self, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = UserApp.objects.filter(rol_teacher=3)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RolForm(forms.ModelForm):
    class Meta:
        model = Roles
        fields = ('description',)

    def __init__(self, *args, **kwargs):
        super(RolForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class GenerateAssignation(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ('id_student', 'year')

    def __init__(self, *args, **kwargs):
        super(GenerateAssignation, self).__init__(*args, **kwargs)
        year:int = datetime.now().year
        self.fields['id_student'].queryset = UserApp.objects.filter(
            rol_teacher=4)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AssignateCourse(forms.ModelForm):
    class Meta:
        model = CursoAsignacion
        fields = ('curso', 'asignacion')

    def __init__(self, *args, **kwargs):
        super(AssignateCourse, self).__init__(*args, **kwargs)
        self.fields['asignacion'].queryset = Asignacion.objects.filter(year__gte=2021)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AssignRol(forms.ModelForm):
    class Meta:
        model = UserApp
        fields = ('rol_teacher',)

    def __init__(self, *args, **kwargs):
        super(AssignRol, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FormCrearTarea(forms.ModelForm):

    class Meta:
        model = Tareas
        fields = ('title','description', 'curso', 'valor', 'fecha_de_entrega',)

    fecha_de_entrega = forms.DateField()


    def __init__(self, *args, **kwargs):
        query = Curso.objects.filter(id_curso=kwargs.pop('pk'))
        super(FormCrearTarea, self).__init__(*args, **kwargs)
        self.fields['curso'].queryset = query
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FormSubirTarea(forms.ModelForm):
    class Meta:
        model = EntregaTareas
        fields = ('archivo_asociado',)

    def __init__(self, *args, **kwargs):
        super(FormSubirTarea, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FormCalificarTarea(forms.ModelForm):
    class Meta:
        model = EntregaTareas
        fields = ('calificacion',)

    def __init__(self,*args,**kwargs):
        super(FormCalificarTarea, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
