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
    path('update-program/<int:pk>/', views.update_program, name='update-program'),
    path('programs/', views.list_program, name='list-program'),
]
