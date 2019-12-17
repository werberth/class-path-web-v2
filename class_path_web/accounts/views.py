from django.urls import reverse_lazy as r
from django.shortcuts import render, redirect

from . import forms, models


def signup(request):
    success_url = r('core:home')
    template_name = 'accounts/signup.html'
    user_form = forms.CustomUserCreationForm()
    institution_form = forms.InstitutionForm()

    if request.method == "POST":
        user_form = forms.CustomUserCreationForm(request.POST)
        institution_form = forms.InstitutionForm(request.POST)

        if institution_form.is_valid() and user_form.is_valid():
            # create instances
            institution = institution_form.save()
            user = user_form.save()
            # define this user as admin of this that institution
            models.Admin.objects.create(user=user, institution=institution)
            return redirect(success_url)

    context = {
        'institution_form': institution_form,
        'user_form': user_form
    }
    return render(request, template_name, context)
