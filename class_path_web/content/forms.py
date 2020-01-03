from django.forms import ModelForm

from . import models

class ContentForm(ModelForm):
    class Meta:
        model = models.Content
        fields = (
            'title', 'description',
        )
