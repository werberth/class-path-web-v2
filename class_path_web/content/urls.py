from django.urls import path

from . import views


urlpatterns = [
    path('create-content/', views.create_content, name='create-content'),
]
