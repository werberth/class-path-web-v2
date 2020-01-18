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
            'content', 'course', 'class_id', 'multimedia_required'
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = self.get_courses()
        self.fields['class_id'].queryset = self.get_field_queryset('classes')
        self.fields['location'].queryset = self.get_field_queryset('locations')
        self.fields['content'].queryset = self.get_field_queryset('contents')

        if self.request.user.has_institution:
            self.fields['class_id'].required = False
        else:
            self.fields['course'].required = False

    def get_field_queryset(self, attr):
        teacher = self.request.user.teacher
        queryset = getattr(teacher, attr).all()
        return queryset

    def get_courses(self):
        teacher = self.request.user.teacher
        return teacher.courses.all()
