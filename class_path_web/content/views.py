from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from django.urls import reverse_lazy as r
from django.utils.decorators import method_decorator

from ..core import base_views as base_core_views
from . import base_views, forms


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_teacher'), name='dispatch')
class CreateContentView(base_core_views.BaseFormView, generic.CreateView):
    form_class = forms.ContentForm
    template_title = 'Criar Conteudo'
    success_url = r('content:list-content')
    template_name = 'content/content_form.html'

    def form_valid(self, form):
        content = form.save(commit=False)
        content.teacher = self.request.user.teacher
        self.object = content.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_teacher'), name='dispatch')
class CreateActivityView(base_core_views.BaseFormView, generic.CreateView):
    form_class = forms.ActivityForm
    template_title = 'Criar Atividade'
    success_url = r('core:dashboard')
    template_name = 'content/activity/activity_form.html'

    def get_form_kwargs(self):
        kwargs = super(CreateActivityView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_teacher'), name='dispatch')
class UpdateContentView(
    base_views.ContentBaseQueryset,
    base_core_views.BaseFormView,
    generic.UpdateView):
    form_class = forms.ContentForm
    success_url = r('content:list-content')
    template_title = 'Editar Conteúdo'
    template_name = 'content/content_form.html'
    context_object_name = 'content'


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_teacher'), name='dispatch')
class ListLocationView(base_views.ContentBaseQueryset, generic.ListView):
    context_object_name = 'contents'
    template_name = 'location/content_list.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_teacher'), name='dispatch')
class DeleteLocationView(
    base_views.ContentBaseQueryset,
    base_core_views.BaseDelete):

    success_url = r('content:list-content')


create_content = CreateContentView.as_view()
create_activity = CreateActivityView.as_view()
update_content = UpdateContentView.as_view()
list_content = ListLocationView.as_view()
delete_content = DeleteLocationView.as_view()
