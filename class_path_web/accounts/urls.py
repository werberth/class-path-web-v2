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
    path('create-program/', views.CreateProgram.as_view(), name='create-program'),
    path('programs/', views.ListPrograms.as_view(), name='program-list'),
]
