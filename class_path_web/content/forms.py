from django.forms import ModelForm

from . import models

class ContentForm(ModelForm):
    class Meta:
        model = models.Content
        fields = (
            'title', 'description',
        )


class ActivityForm(ModelForm):
    class Meta:
        model = models.Activity
        fields = (
            'title', 'description', 'location',
            'content', 'course', 'multimedia_required'
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = self.get_field_queryset('locations')
        self.fields['content'].queryset = self.get_field_queryset('contents')
        self.fields['course'].queryset = self.get_classes()

    def get_field_queryset(self, attr):
        teacher = self.request.user.teacher
        queryset = getattr(teacher, attr).all()
        return queryset

    def get_course(self):
        teacher = self.request.user.teacher
        return teacher.courses.all()
