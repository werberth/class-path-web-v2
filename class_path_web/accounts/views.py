from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy as r
from django.utils.decorators import method_decorator
from django.views import generic

from . import base_views, forms, models

# FBVs

@transaction.atomic
def signup(request):
    success_url = r('core:login')
    template_name = 'accounts/signup.html'
    user_form = forms.CustomUserCreationForm()
    institution_form = forms.InstitutionForm()

    if request.user.is_authenticated():
        return redirect(r('core:dashboard'))

    if request.method == "POST":
        user_form = forms.CustomUserCreationForm(request.POST)
        institution_form = forms.InstitutionForm(request.POST)

        if institution_form.is_valid() and user_form.is_valid():
            # create institution
            institution = institution_form.save()
            # create admin user
            user_form.cleaned_data['is_admin'] = True
            user = user_form.save()
            return redirect(success_url)

    context = {
        'institution_form': institution_form,
        'user_form': user_form
    }
    return render(request, template_name, context)

@transaction.atomic
def update_teacher(request, pk):
    success_url = r('accounts:list-teacher')
    template_title = 'Editar Profesor'
    template_name = 'accounts/teacher/teacher_form.html'

    teacher = get_object_or_404(models.Teacher, pk=pk)
    user_form = forms.CustomUserUpdateForm(
        request.POST or None,
        instance=teacher.user
    )
    teacher_form = forms.TeacherForm(
        request.POST or None,
        instance=teacher
    )

    if user_form.is_valid() and teacher_form.is_valid():
        user_form.save()
        teacher_form.save()
        return redirect(success_url)

    context = {
        'form': user_form,
        'teacher_form': teacher_form,
        'template_title': template_title,
    }
    return render(request, template_name, context)


# CBVs

@method_decorator(login_required, name='dispatch')
class CreateProgram(base_views.BaseFormView, generic.CreateView):
    form_class = forms.ProgramForm
    success_url = r('accounts:list-program')
    template_title = 'Criar Curso'
    template_name = 'accounts/program/program_form.html'

    def form_valid(self, form):
        program = form.save(commit=False)
        program.institution = self.request.user.admin.institution
        self.object = program.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class CreateTeacher(base_views.BaseFormView, generic.CreateView):
    success_url = r('accounts:list-teacher')
    form_class = forms.CustomUserCreationForm
    template_title = 'Criar Professor'
    template_name = 'accounts/teacher/teacher_form.html'

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    @transaction.atomic
    def form_valid(self, form):
        institution = self.request.user.admin.institution

        form.cleaned_data['is_teacher'] = True
        self.object = form.save()

        teacher = models.Teacher.objects.create(
            user=self.object,
            institution=institution
        )
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class CreateClass(base_views.BaseFormView, generic.CreateView):
    form_class = forms.ClassForm
    template_title = 'Criar Turma'
    template_name = 'accounts/class/class_form.html'

    def get_object(self, queryset=None):
        program_id = self.kwargs['program']
        return get_object_or_404(models.Program, pk=program_id)

    def get_context_data(self,**kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['program'] = self.program
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = None
        self.program = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.program = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        class_instance = form.save(commit=False)
        class_instance.program = self.program
        self.object = class_instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        url = r('accounts:list-class', kwargs={'program': self.object.program.id})
        return url


class ListTeacher(base_views.BaseInstitutionQuerysetView, generic.ListView):
    model = models.Teacher
    template_name = 'accounts/teacher/teacher_list.html'
    context_object_name = 'teachers'


@method_decorator(login_required, name='dispatch')
class ListProgram(base_views.BaseInstitutionQuerysetView, generic.ListView):
    model = models.Program
    template_name = 'accounts/program/program_list.html'
    context_object_name = 'programs'


@method_decorator(login_required, name='dispatch')
class ListProgram(base_views.BaseInstitutionQuerysetView, generic.ListView):
    model = models.Program
    template_name = 'accounts/program/program_list.html'
    context_object_name = 'programs'


@method_decorator(login_required, name='dispatch')
class UpdateProgram(
    base_views.BaseFormView,
    base_views.BaseInstitutionQuerysetView,
    generic.UpdateView):

    model = models.Program
    form_class = forms.ProgramForm
    success_url = r('accounts:list-program')
    template_title = 'Editar Curso'
    template_name = 'accounts/program/program_form.html'
    context_object_name = 'program'


@method_decorator(login_required, name='dispatch')
class UpdateClass(base_views.BaseFormView, generic.UpdateView):
    form_class = forms.ClassForm
    template_title = 'Editar Turma'
    template_name = 'accounts/class/class_form.html'
    context_object_name = 'class'

    def get_queryset(self):
        programs = self.request.user.admin.institution.programs.all()
        classes = models.Class.objects.filter(program__in=programs)
        return classes

    def get_success_url(self):
        url = r('accounts:list-class', kwargs={'program': self.object.program.id})
        return url


class ClassList(generic.ListView):
    model = models.Class
    context_object_name = 'classes'
    template_name = 'accounts/class/class_list.html'

    def get_object(self, queryset=None):
        program_id = self.kwargs['program']
        return get_object_or_404(models.Program, pk=program_id)

    def get_context_data(self,**kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['program'] = self.program
        return kwargs

    def get(self, request, *args, **kwargs):
        self.program = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.program.classes.all()


class DeleteClassView(generic.DeleteView):

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        institution = self.request.user.admin.institution
        programs = institution.programs.all()
        return models.Class.objects.filter(program__in=programs)

    def get_success_url(self):
        url = r('accounts:list-class', kwargs={'program': self.object.program.id})
        return url


# define CBVs as FBVs
# create
create_program = CreateProgram.as_view()
create_class = CreateClass.as_view()
create_teacher = CreateTeacher.as_view()
# update
update_program = UpdateProgram.as_view()
update_class = UpdateClass.as_view()
# list
list_program = ListProgram.as_view()
list_teacher = ListTeacher.as_view()
list_class = ClassList.as_view()
# delete
delete_class = DeleteClassView.as_view()
