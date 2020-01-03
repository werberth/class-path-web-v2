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


class ListLocationView(generic.ListView):
    context_object_name = 'locations'
    template_name = 'location/location_list.html'

    def get_queryset(self):
        teacher = self.request.user.teacher
        locations = teacher.locations.all()
        return locations


create_location = CreateLocationView.as_view()
list_location = ListLocationView.as_view()
