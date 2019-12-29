from . import models

from django.views import generic

class BaseInstitutionQuerysetView:
    def get_queryset(self):
        institution = self.request.user.admin.institution
        queryset = self.model.objects.filter(institution=institution)
        return queryset


class BaseFormView:
    template_title = None

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['template_title'] = self.template_title
        return kwargs