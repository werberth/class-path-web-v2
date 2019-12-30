from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('api/', include(('class_path_web.accounts.api.urls', 'core'), namespace="core")),
    path('sign-up/', views.signup, name='sign-up'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            redirect_authenticated_user=True
        ),
        name="login"
    ),
    # create
    path('create-program/', views.create_program, name='create-program'),
    path('create-teacher/', views.create_teacher, name='create-teacher'),
    path('create-class/<int:program>/', views.create_class, name='create-class'),
    path('create-student/<int:class>/', views.create_student, name='create-student'),
    # update
    path('update-program/<int:pk>/', views.update_program, name='update-program'),
    path('update-teacher/<int:pk>/', views.update_teacher, name='update-teacher'),
    path('update_class/<int:pk>/', views.update_class, name='update-class'),
    path('update-student/<int:pk>/', views.update_student, name='update-student'),
    # list
    path('programs/', views.list_program, name='list-program'),
    path('teachers/', views.list_teacher, name='list-teacher'),
    path('classes/<int:program>/', views.list_class, name='list-class'),
    path('students/<int:class>/', views.list_student, name='list-student'),
    # delete
    path('delete-class/<int:pk>/', views.delete_class, name='delete-class'),
    path('delete-teacher/<int:pk>/', views.delete_teacher, name='delete-teacher'),
]
