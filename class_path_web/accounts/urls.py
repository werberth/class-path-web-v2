from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('sign-up/', views.signup, name='sign-up'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name="login"
    ),
    path('create-program/', views.create_program, name='create-program'),
    path('create-teacher/', views.create_teacher, name='create-teacher'),
    path('create-class/<int:program>/', views.create_class, name='create-class'),
    path('update-program/<int:pk>/', views.update_program, name='update-program'),
    path('update-teacher/<int:pk>/', views.update_teacher, name='update-teacher'),
    path('programs/', views.list_program, name='list-program'),
    path('teachers/', views.list_teacher, name='list-teacher'),
]
