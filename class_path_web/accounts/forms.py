from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from . import models


class InstitutionForm(ModelForm):
    class Meta:
        model = models.Institution
        fields = (
            'name', 'description',
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = (
            "registration_number", "email",
            "first_name", "last_name",
        )

    def get_process_cleaned_data(self):
        data = self.cleaned_data.copy()

        del data['password2']

        data['is_admin'] = True
        data['password'] = data.pop('password1')
        return data

    def save(self):
        # define user permission field
        data = self.get_process_cleaned_data()
        print(data)
        # create user
        user = models.User.objects.create_user(**data)
        return user
