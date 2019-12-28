from . import models

class BaseProgramView:
    def get_queryset(self):
        institution = self.request.user.admin.institution
        queryset = models.Program.objects.filter(institution=institution)
        return queryset