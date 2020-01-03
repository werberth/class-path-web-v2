from . import models

from django.views import generic


class BaseInstitutionQuerysetView:
    def get_queryset(self):
        institution = self.request.user.admin.institution
        queryset = self.model.objects.filter(institution=institution)
        return queryset


class BaseDelete(generic.DeleteView):
    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BaseFormView:
    template_title = None

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['template_title'] = self.template_title
        return kwargs


class ListCourseBase(generic.ListView):
    model = models.Course
    context_object_name = 'courses'
    template_name = 'accounts/course/course_list.html'