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

    def process_cleaned_data(self):
        data = self.cleaned_data.copy()

        del data['password2']

        data['password'] = data.pop('password1')
        return data

    def save(self):
        # define user permission field
        data = self.process_cleaned_data()
        # create user
        user = models.User.objects.create_user(**data)
        return user


class CustomUserUpdateForm(ModelForm):
    class Meta:
        model = models.User
        fields = (
            "registration_number", "email",
            "first_name", "last_name",
        )


class TeacherForm(ModelForm):
    class Meta:
        model = models.Teacher
        fields = (
            'cpf', 'description',
        )


class ProgramForm(ModelForm):
    class Meta:
        model = models.Program
        fields = (
            'name', 'description'
        )


class ClassForm(ModelForm):
    class Meta:
        model = models.Class
        fields = (
            'name', 'description'
        )


class CourseForm(ModelForm):
    class Meta:
        model = models.Course
        fields = (
            'name', 'description',
            'teacher'
        )


class ScoreForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_score'].required = False
        self.fields['second_score'].required = False
        self.fields['third_score'].required = False

    class Meta:
        model = models.Scores
        fields = (
            'first_score', 'second_score',
            'third_score',
        )