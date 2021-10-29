from django.db.models import F
from django.shortcuts import render, get_list_or_404, redirect
from .forms import *
from datetime import timezone, datetime
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.cache import caches
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView, ListView, UpdateView
from django.urls import reverse_lazy
from .tables import TableButton
from django_tables2 import SingleTableView


class UsuarioNuevo(CreateView):
    form_class = FormUser
    template_name = 'registration/register.html'
    success_url = reverse_lazy('asignacion')


class TableCalifications(LoginRequiredMixin, SingleTableView):
    template_name = 'tabla.html'
    # table_class = TableButton
    model = CursoAsignacion

    def get_queryset(self, *args, **kwargs):
        query = CursoAsignacion.objects.select_related().filter(curso__id_curso=self.kwargs['pk'])
        return get_list_or_404(query)

    def get_context_data(self, **kwargs):
        context = super(TableCalifications, self).get_context_data(**kwargs)
        context['title'] = 'Calificaciones'
        return context


class CreateCurso(LoginRequiredMixin, CreateView):
    form_class = CursoForm
    template_name = 'create_update.shtml'
    success_url = reverse_lazy('inicio')

    def get_context_data(self, **kwargs):
        context = super(CreateCurso, self).get_context_data(**kwargs)
        context['title'] = 'Crear Curso'
        return context


class AsignarRol(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    form_class = AssignRol
    model = UserApp
    template_name = 'create_update.html'
    success_url = reverse_lazy('inicio')

    def handle_no_permission(self):
        return redirect('403')

    def test_func(self):
        return self.request.user.userapp.rol_teacher.id_rol == 1

    def get_context_data(self, **kwargs):
        context = super(AsignarRol, self).get_context_data(**kwargs)
        usuario = UserApp.objects.filter(id=self.kwargs['pk']).get()
        context['title'] = f'Asignar Rol   {usuario}'
        context['is_valid'] = True
        return context


class ViewSubirTarea(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = 'create_update.html'
    model = EntregaTareas
    success_url = reverse_lazy('inicio')
    form_class = FormSubirTarea

    def form_valid(self, form):
        object = form.save(commit=False)
        form.alumno = self.request.user.userapp
        form.tarea = Tareas.objects.filter(id_tarea=self.kwargs['pk'])[0]
        form.fecha_de_subida = datetime.now(timezone.utc)
        form.save()
        return super(ViewSubirTarea, self).form_valid(form)

    def handle_no_permission(self):
        return redirect('403')

    def test_func(self):
        return self.request.user.userapp.rol_teacher.id_rol == 4

    # def form_valid(self, form):
    #     fecha = Tareas.objects.filters()
    #     messages.error(self.request, 'no es una fecha valida')
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ViewSubirTarea, self).get_context_data(**kwargs)
        resultado = Tareas.objects.filter(id_tarea=self.kwargs['pk']).values('fecha_de_entrega', 'title', 'description')
        existe = EntregaTareas.objects.filter(tarea=self.kwargs['pk'], alumno=self.request.user.userapp).count()
        contenido = resultado[0]
        title = contenido['title']
        description = contenido['description']
        date_current: datetime = datetime.now(timezone.utc)
        isValid: bool = contenido['fecha_de_entrega'] < date_current
        context['title'] = f' {title} '
        context['fecha'] = contenido['fecha_de_entrega']
        context['description'] = description
        context['is_valid'] = isValid and existe == 0
        return context


class ViewCrearTarea(CreateView):
    template_name = 'create_update.html'
    success_url = reverse_lazy('inicio')
    form_class = FormCrearTarea

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs



    def get_context_data(self, **kwargs):
        context = super(ViewCrearTarea, self).get_context_data(**kwargs)
        context['title'] = 'Crear Tarea'
        context['is_valid'] = True
        return context


class ListaTareas(ListView):
    model = Tareas
    template_name = 'lista.html'
    paginate_by = 7

    def get_queryset(self, *args, **kwargs):
        return get_list_or_404(Tareas.objects.filter(curso=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        context = super(ListaTareas, self).get_context_data(**kwargs)
        context['title'] = 'Listar Tareas'
        context['tareas'] = True
        rol: int = self.request.user.userapp.rol_teacher.id_rol
        context['is_alumno'] = rol == 4
        context['is_teacher'] = rol == 3
        return context


class CreateAsignacion(LoginRequiredMixin, CreateView):
    template_name = 'create_update.html'
    success_url = reverse_lazy('inicio')
    form_class = AssignateCourse

    def get_context_data(self, **kwargs):
        context = super(CreateAsignacion, self).get_context_data(**kwargs)
        context['title'] = 'Asignar Curso'
        context['is_valid'] = True
        return context


class CreateRol(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    form_class = RolForm
    template_name = 'create_update.html'
    success_url = reverse_lazy('inicio')

    def test_func(self):
        return self.request.user.userapp.rol_teacher.id_rol == 1

    def handle_no_permission(self):
        return redirect('inicio')

    def get_context_data(self, **kwargs):
        context = super(CreateRol, self).get_context_data(**kwargs)
        context['title'] = 'Crear Rol'
        return context


class ListCursos(ListView):
    model = Curso
    template_name = 'lista.html'
    paginate_by = 7

    def get_queryset(self, *args, **kwargs):
        return get_list_or_404(Curso.objects.get)


class ListStudent(LoginRequiredMixin, ListView):
    model = UserApp
    template_name = 'lista.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        return get_list_or_404(UserApp.objects.all().filter(rol_teacher=3))

    def get_context_data(self, **kwargs):
        context = super(ListStudent, self).get_context_data(**kwargs)
        context['title'] = 'Estudiantes'
        context['list_student'] = True
        return context


class ListStudentsCourse(LoginRequiredMixin, ListView):
    template_name = 'lista.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        query = UserApp.objects.filter()
        return get_list_or_404(query)

    def get_context_data(self, **kwargs):
        context = super(ListStudentsCourse, self).get_context_data(**kwargs)
        context['title'] = 'Alumnos Asignados a Cursos'
        context['is_course'] = True
        context['subject_id'] = self.kwargs['pk']
        return context


class RegistrarAsignacion(CreateView):
    template_name = 'create_update.html'
    form_class = GenerateAssignation
    success_url = reverse_lazy('asignarCurso')

    def get_context_data(self, **kwargs):
        context = super(RegistrarAsignacion, self).get_context_data(**kwargs)
        context['title'] = 'Registrar Inscripcion'
        context['is_valid'] = True
        return context


def home(request):
    return redirect('login')


def perfil(request):
    return render(request, 'registration/accounts_profile.html')


class HomeLogin(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeLogin, self).get_context_data(**kwargs)
        user_app = self.request.user.userapp
        rol_current_user: int = user_app.rol_teacher.id_rol
        is_admin: bool = rol_current_user == 1
        is_student: bool = rol_current_user == 4
        is_teacher: bool = rol_current_user == 3
        if is_teacher:
            context['object_list'] = Curso.objects.filter(teacher=user_app)
            context['is_teacher'] = is_teacher
        if is_student:
            year: int = datetime.now().year
            asignacion = Asignacion.objects.filter(id_student=user_app, year=year).get()
            context['object_list'] = CursoAsignacion.objects.filter(asignacion=asignacion.id_asignacion)
        return context


def prohibido(request):
    return render(request, '403.html')


# Create your views here.

class ViewCalificarTarea(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    form_class = FormCalificarTarea
    model = EntregaTareas
    template_name = 'create_update.html'
    success_url = reverse_lazy('inicio')


    def form_valid(self, form):
        calificacion_tarea = form.cleaned_data['calificacion']
        year: int = datetime.now().year
        codigo_entrega = self.kwargs['pk']
        entrega = EntregaTareas.objects.filter(codigo_tarea=codigo_entrega).get()
        curso = entrega.tarea.curso
        alumno = entrega.alumno
        asignacion = Asignacion.objects.filter(year=year, id_student=alumno)
        obtener = asignacion.get()
        CursoAsignacion.objects.filter(curso=curso, asignacion=obtener).update(F('tareas') + calificacion_tarea)
        return super(ViewCalificarTarea, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ViewCalificarTarea, self).get_context_data(**kwargs)
        context['title'] = f'Calificar'
        context['is_valid'] = True
        return context
