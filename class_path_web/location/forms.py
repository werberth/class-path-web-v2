from django.forms import ModelForm

from . import models

class LocationForm(ModelForm):
    class Meta:
        model = models.Location
        fields = (
            'name', 'description', 'latitude',
            'longitude'
        )
