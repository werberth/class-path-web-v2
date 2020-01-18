from django.views import generic
from django.shortcuts import get_object_or_404

from . import models


class BaseInstitutionQuerysetView:
    def get_queryset(self):
        institution = self.request.user.admin.institution
        queryset = self.model.objects.filter(institution=institution)
        return queryset


class ListCourseBase(generic.ListView):
    model = models.Course
    context_object_name = 'courses'
    template_name = 'accounts/course/course_list.html'


class ListStudentBase:
    context_object_name = 'students'
    template_name = 'accounts/student/student_list.html'

    @property
    def class_instance(self):
        if self.request.user.has_institution:

            if self.request.user.is_teacher:
                institution = self.request.user.teacher.institution
            else:
                institution = self.request.user.admin.institution

            programs = institution.programs.values_list('id', flat=True)
            class_ = get_object_or_404(
                models.Class,
                pk=self.kwargs['class'],
                program__in=programs
            )
            return class_

        return get_object_or_404(
                models.Class,
                pk=self.kwargs['class'],
                teacher=self.request.user.teacher
            )

    def get_context_data(self,**kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['class'] = self.class_instance
        return kwargs

    def get_queryset(self):
        return self.class_instance.students.filter(is_active=True)
