from datetime import datetime

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db.models import Sum

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


class EmailForm(forms.Form):
    destinatario = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EmailandRol(forms.ModelForm):
    class Meta:
        model = UserApp
        fields = ('parent_email', 'rol_teacher')

    def __init__(self, *args, **kwargs):
        super(EmailandRol, self).__init__(*args, **kwargs)
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
        year: int = datetime.now().year
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
        fields = ('title', 'description', 'curso', 'valor', 'fecha_de_entrega',)

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
        fields = ('calificacion', 'archivo_asociado')

    def clean(self):
        cleaned_data = super(FormCalificarTarea, self).clean()
        query = EntregaTareas.objects.filter(codigo_tarea=self.identifier).values('tarea')
        id_tarea = query[0]['tarea']
        valor_maximo = Tareas.objects.filter(id_tarea=id_tarea).values('valor')[0]['valor']
        valor_actual = cleaned_data.get('calificacion')
        if valor_actual < 0 or valor_actual > valor_maximo:
            raise forms.ValidationError(f"Debe ingresar un valor mayor o igual a 0 y menor o igual a "
                                        f"{valor_maximo}")

    def __init__(self, *args, **kwargs):
        self.identifier = kwargs.pop('pk')
        super(FormCalificarTarea, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FormCalificar(forms.ModelForm):
    total = forms.IntegerField(disabled=True)
    tareas = forms.IntegerField(disabled=True)

    class Meta:
        model = CursoAsignacion
        fields = ('asignacion', 'tareas', 'primer_parcial', 'segundo_parcial', 'final', 'total',)

    def __init__(self, *args, **kwargs):
        self.identificador = kwargs.pop('identificador')
        super(FormCalificar, self).__init__(*args, **kwargs)
        valid_set = CursoAsignacion.objects.filter(id_curso_asignacion=self.identificador)
        self.fields['tareas'].queryset = valid_set
        self.fields['total'].queryset = valid_set
        self.fields['total'].initial = valid_set.get().total
        self.fields['tareas'].initial = valid_set.get().tareas
        id_asignacion = valid_set.get().asignacion.id_asignacion
        self.fields['asignacion'].queryset= Asignacion.objects.filter(id_asignacion=id_asignacion)
        #self.fields['asignacion'].queryset = Asignacion.objects.filter()
        #self.fields['tareas'].queryset = EntregaTareas.objects.filter(alumno=self.student, tarea__curso=self.curso).\
         #   aggregate(Sum('calificacion'))
        #year: int = datetime.now().year
        #asignation = Asignacion.objects.filter(id_student=self.student, year=year)
        #self.fields['asignacion'].queryset = asignation
        #self.fields['total'].queryset = CursoAsignacion.objects.filter(asignacion=asignation,
                    #                                                   curso=self.curso).get().total
        # self.fields['total'].queryset = CursoAsignacion.objects.filter(asignacion=).get().total()

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'







class FormEditProfile(UserChangeForm):
    email = forms.EmailField(label='Correo Electronico', widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label='Nombre', max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label='Usuario', max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label='Apellido', max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    is_active = forms.CharField(label='activo', max_length=100,
                                widget=forms.CheckboxInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('email', 'username', 'last_name', 'first_name', 'is_active', 'password')
