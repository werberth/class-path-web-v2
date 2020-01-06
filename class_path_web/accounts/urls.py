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
    path('create-course/<int:class>/', views.create_course, name='create-course'),
    path('create-address/', views.create_address, name='create_address'),
    # update
    path('update-program/<int:pk>/', views.update_program, name='update-program'),
    path('update-teacher/<int:pk>/', views.update_teacher, name='update-teacher'),
    path('update_class/<int:pk>/', views.update_class, name='update-class'),
    path('update-student/<int:pk>/', views.update_student, name='update-student'),
    path('update-course/<int:pk>/', views.update_course, name='update-course'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-address/<int:pk>/', views.update_address, name='update_address'),
    path(
        'define-scores/<int:student>/<int:course>/',
        views.define_scores,
        name='define-scores'
    ),
    # list
    path('programs/', views.list_program, name='list-program'),
    path('teachers/', views.list_teacher, name='list-teacher'),
    path('teacher-courses/', views.list_teacher_courses, name='list-teacher-courses'),
    path('classes/<int:program>/', views.list_class, name='list-class'),
    path('class/<int:course>/', views.list_class_students, name='list-class-students'),
    path('students/<int:class>/', views.list_student, name='list-student'),
    path('courses/<int:class>/', views.list_course, name='list-course'),
    # delete
    path('delete-program/<int:pk>/', views.delete_program, name='delete-program'),
    path('delete-class/<int:pk>/', views.delete_class, name='delete-class'),
    path('delete-teacher/<int:pk>/', views.delete_teacher, name='delete-teacher'),
    path('delete-student/<int:pk>/', views.delete_student, name='delete-student'),
    path('delete-course/<int:pk>/', views.delete_course, name='delete-course'),
    path('delete-address/<int:pk>/', views.delete_address, name='delete-address'),
    # detail
    path('profile/', views.profile_view, name='profile'),
]
