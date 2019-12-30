
from .models import Class

def get_classes(user):
    institution = user.admin.institution
    program_ids = institution.programs.values_list('id', flat=True)
    classes = Class.objects.filter(program__in=program_ids)
    return classes.values_list('id', flat=True)
