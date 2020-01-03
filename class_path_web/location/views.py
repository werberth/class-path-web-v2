from django.views import generic

from django.urls import reverse_lazy as r

from ..core import base_views
from . import models, forms


class CreateLocationView(base_views.BaseFormView, generic.CreateView):
    form_class = forms.LocationForm
    template_title = 'Criar Localização'
    success_url = r('core:dashboard')
    template_name = 'location/location_form.html'

    def form_valid(self, form):
        location = form.save(commit=False)
        location.teacher = self.request.user.teacher
        self.object = location.save()
        return super().form_valid(form)


create_location = CreateLocationView.as_view()