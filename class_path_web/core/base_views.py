from django.views import generic


class BaseDelete(generic.DeleteView):
    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BaseFormView:
    template_title = None

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['template_title'] = self.template_title
        return kwargs