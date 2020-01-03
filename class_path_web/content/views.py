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
    success_url = r('core:dashboard')
    template_name = 'content/content_form.html'

    def form_valid(self, form):
        content = form.save(commit=False)
        content.teacher = self.request.user.teacher
        self.object = content.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('accounts.is_teacher'), name='dispatch')
class ListLocationView(base_views.ContentBaseQueryset, generic.ListView):
    context_object_name = 'contents'
    template_name = 'location/content_list.html'


create_content = CreateContentView.as_view()
list_content = ListLocationView.as_view()
