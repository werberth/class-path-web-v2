from . import models


class ContentBaseQueryset:

    def get_queryset(self):
        teacher = self.request.user.teacher
        contents = teacher.contents.all()
        return contents


class ActivityBaseQueryset:

    def get_queryset(self):
        teacher = self.request.user.teacher
        contents = teacher.contents.values_list('id', flat=True)
        activities = models.Activity.objects.filter(content__id__in=contents)
        return activities