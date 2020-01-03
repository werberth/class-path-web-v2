from django.views import generic

from django.urls import reverse_lazy as r

from ..core import base_views as base_core_views
from . import base_views, forms, models


class CreateLocationView(base_core_views.BaseFormView, generic.CreateView):
    form_class = forms.LocationForm
    template_title = 'Criar Localização'
    success_url = r('location:list-location')
    template_name = 'location/location_form.html'

    def form_valid(self, form):
        location = form.save(commit=False)
        location.teacher = self.request.user.teacher
        self.object = location.save()
        return super().form_valid(form)


class UpdateLocationView(
    base_views.LocationBaseQueryset,
    base_core_views.BaseFormView,
    generic.UpdateView):
    form_class = forms.LocationForm
    success_url = r('location:list-location')
    template_title = 'Editar Localização'
    template_name = 'location/location_form.html'
    context_object_name = 'location'


class ListLocationView(base_views.LocationBaseQueryset, generic.ListView):
    context_object_name = 'locations'
    template_name = 'location/location_list.html'


class DeleteLocationView(
    base_views.LocationBaseQueryset,
    base_core_views.BaseDelete):

    success_url = r('location:list-location')

create_location = CreateLocationView.as_view()
update_location = UpdateLocationView.as_view()
delete_location = DeleteLocationView.as_view()
list_location = ListLocationView.as_view()
