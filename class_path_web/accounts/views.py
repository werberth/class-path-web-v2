from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy as r
from django.utils.decorators import method_decorator
from django.views import generic

from ..core import base_views as base_core_views
from . import base_views, forms, models, utils

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
@login_required
@permission_required('accounts.is_admin')
def update_teacher(request, pk):
    success_url = r('accounts:list-teacher')
    template_title = 'Editar Profesor'
    template_name = 'accounts/teacher/teacher_form.html'

    institution = request.user.admin.institution
    teacher = get_object_or_404(
        models.Teacher,
        pk=pk,
        institution=institution,
    )

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

@transaction.atomic
@login_required
@permission_required('accounts.is_admin')
def update_student(request, pk):
    template_title = 'Editar Student'
    template_name = 'accounts/student/student_form.html'

    classes_id = utils.get_classes(request.user)
    student = get_object_or_404(
        models.Student,
        pk=pk,
        class_id__in=classes_id
    )

    user_form = forms.CustomUserUpdateForm(
        request.POST or None,
        instance=student.user
    )
    student_form = forms.TeacherForm(
        request.POST or None,
        instance=student
    )

    if user_form.is_valid() and student_form.is_valid():
        user_form.save()
        student_form.save()
        success_url = r(
            'accounts:list-student',
            kwargs={'class': student.class_id.pk}
        )
        return redirect(success_url)

    context = {
        'form': user_form,
        'class': student.class_id,
        'student_form': student_form,
        'template_title': template_title,
    }
    return render(request, template_name, context)


# CBVs

# Create Views

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class CreateProgram(base_core_views.BaseFormView, generic.CreateView):
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
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class CreateTeacher(base_core_views.BaseFormView, generic.CreateView):
    success_url = r('accounts:list-teacher')
    form_class = forms.CustomUserCreationForm
    template_title = 'Criar Professor'
    template_name = 'accounts/teacher/teacher_form.html'

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
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class CreateStudent(base_core_views.BaseFormView, generic.CreateView):
    form_class = forms.CustomUserCreationForm
    template_title = 'Criar Estudante'
    template_name = 'accounts/student/student_form.html'

    @property
    def _class(self):
        institution = self.request.user.admin.institution
        programs = institution.programs.values_list('id', flat=True)
        class_instance = get_object_or_404(
            models.Class,
            pk=self.kwargs['class'],
            program__in=programs
        )
        return class_instance

    @transaction.atomic
    def form_valid(self, form):
        institution = self.request.user.admin.institution

        form.cleaned_data['is_student'] = True
        self.object = form.save()

        student = models.Student.objects.create(
            user=self.object,
            class_id=self._class
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self,**kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['class'] = self._class
        return kwargs

    def get_success_url(self):
        url = r('accounts:list-student', kwargs={'class': self._class.id})
        return url


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class CreateClass(base_core_views.BaseFormView, generic.CreateView):
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


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class CreateCourse(base_core_views.BaseFormView, generic.CreateView):
    form_class = forms.CourseForm
    template_title = 'Criar Disciplina'
    template_name = 'accounts/course/course_form.html'

    @property
    def _class(self):
        institution = self.request.user.admin.institution
        programs = institution.programs.values_list('id', flat=True)
        class_instance = get_object_or_404(
            models.Class,
            pk=self.kwargs['class'],
            program__in=programs
        )
        return class_instance

    def form_valid(self, form):
        course = form.save(commit=False)
        course.class_id = self._class
        self.object = course.save()
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['class'] = self._class
        return kwargs

    def get_success_url(self):
        url = r('accounts:list-class', kwargs={'program': self._class.program.id})
        return url


# List Views

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class ListStudent(base_views.ListStudentBase, generic.ListView):

    def get_object(self, queryset=None):
        institution = self.request.user.admin.institution
        program_ids = institution.programs.values_list('id', flat=True)
        _class = get_object_or_404(
            models.Class,
            pk=self.kwargs['class'],
            program__in=program_ids
        )
        return _class


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class ListTeacher(base_views.BaseInstitutionQuerysetView, generic.ListView):
    model = models.Teacher
    template_name = 'accounts/teacher/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class ListProgram(base_views.BaseInstitutionQuerysetView, generic.ListView):
    model = models.Program
    template_name = 'accounts/program/program_list.html'
    context_object_name = 'programs'


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class ListProgram(base_views.BaseInstitutionQuerysetView, generic.ListView):
    model = models.Program
    template_name = 'accounts/program/program_list.html'
    context_object_name = 'programs'


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class ClassList(generic.ListView):
    model = models.Class
    context_object_name = 'classes'
    template_name = 'accounts/class/class_list.html'

    def get_object(self, queryset=None):
        program_id = self.kwargs['program']
        return get_object_or_404(models.Program, pk=program_id)

    def get_context_data(self,**kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['program'] = self.get_object()
        return kwargs

    def get_queryset(self):
        program = self.get_object()
        return program.classes.all()


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class ListCourse(base_views.ListCourseBase):

    def get_object(self, queryset=None):
        return get_object_or_404(models.Class, pk=self.kwargs['class'])

    def get_context_data(self,**kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['class'] = self.get_object()
        return kwargs

    def get_queryset(self):
        class_instance = self.get_object()
        return class_instance.courses.all()


# Update Views


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class UpdateProgram(
    base_core_views.BaseFormView,
    base_views.BaseInstitutionQuerysetView,
    generic.UpdateView):

    model = models.Program
    form_class = forms.ProgramForm
    success_url = r('accounts:list-program')
    template_title = 'Editar Curso'
    template_name = 'accounts/program/program_form.html'
    context_object_name = 'program'


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class UpdateClass(base_core_views.BaseFormView, generic.UpdateView):
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


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class UpdateCourse(base_core_views.BaseFormView, generic.UpdateView):
    form_class = forms.CourseForm
    template_title = 'Editar Disciplina'
    template_name = 'accounts/course/course_form.html'

    def get_queryset(self):
        programs = self.request.user.admin.institution.programs.all()
        classes = models.Class.objects.filter(program__in=programs)
        courses = models.Course.objects.filter(class_id__in=classes)
        return courses

    def get_success_url(self):
        url = r(
            'accounts:list-course',
            kwargs={
                'class': self.object.class_id.id
            }
        )
        return url


# Delete Views


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class DeleteCourseView(base_core_views.BaseDelete):

    def get_queryset(self):
        programs = self.request.user.admin.institution.programs.all()
        classes = models.Class.objects.filter(program__in=programs)
        courses = models.Course.objects.filter(class_id__in=classes)
        return courses

    def get_success_url(self):
        url = r(
            'accounts:list-course',
            kwargs={
                'class': self.object.class_id.id
            }
        )
        return url


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class DeleteClassView(base_core_views.BaseDelete):

    def get_queryset(self):
        institution = self.request.user.admin.institution
        programs = institution.programs.all()
        return models.Class.objects.filter(program__in=programs)

    def get_success_url(self):
        url = r('accounts:list-class', kwargs={'program': self.object.program.id})
        return url


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class DeleteTeacherView(base_core_views.BaseDelete):
    success_url = r('accounts:list-teacher')

    def get_queryset(self):
        institution = self.request.user.admin.institution
        teachers = models.Teacher.objects.filter(institution=institution)
        users_ids = teachers.values_list('user__id', flat=True)
        return models.User.objects.filter(id__in=users_ids)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.teacher.is_active = False

        self.object.teacher.save()
        self.object.save()

        return HttpResponseRedirect(self.success_url)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_admin'), name='dispatch')
class DeleteStudentView(base_core_views.BaseDelete):

    def get_queryset(self):
        classes_id = utils.get_classes(self.request.user)
        students = models.Student.objects.filter(class_id__in=classes_id)
        users_ids = students.values_list('user__id', flat=True)
        return models.User.objects.filter(id__in=users_ids)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.student.is_active = False

        self.object.student.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        url = r(
            'accounts:list-student',
            kwargs={
                'class': self.object.student.class_id.pk
            }
        )
        return url


# Teacher Views

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_teacher'), name='dispatch')
class TeacherListCourse(base_views.ListCourseBase):
    def get_queryset(self):
        teacher = self.request.user.teacher
        courses = models.Course.objects.filter(teacher=teacher)
        return courses


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_teacher'), name='dispatch')
class ListClassStudents(base_views.ListStudentBase, generic.ListView):

    def get_object(self, queryset=None):
        teacher = self.request.user.teacher
        classes = teacher.courses.values_list('class_id__id',flat=True)
        _class = get_object_or_404(
            models.Class,
            pk=self.kwargs['class'],
            pk__in=classes
        )
        return _class


# define CBVs as FBVs
# create
create_program = CreateProgram.as_view()
create_class = CreateClass.as_view()
create_teacher = CreateTeacher.as_view()
create_student = CreateStudent.as_view()
create_course = CreateCourse.as_view()
# update
update_program = UpdateProgram.as_view()
update_class = UpdateClass.as_view()
update_course = UpdateCourse.as_view()
# list
list_program = ListProgram.as_view()
list_teacher = ListTeacher.as_view()
list_class = ClassList.as_view()
list_student = ListStudent.as_view()
list_course = ListCourse.as_view()
list_teacher_courses = TeacherListCourse.as_view()
list_class_students = ListClassStudents.as_view()
# delete
delete_class = DeleteClassView.as_view()
delete_teacher = DeleteTeacherView.as_view()
delete_student = DeleteStudentView.as_view()
delete_course = DeleteCourseView.as_view()
