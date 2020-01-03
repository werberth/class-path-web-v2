from django.urls import path

from . import views


urlpatterns = [
    path('create-content/', views.create_content, name='create-content'),
    path('update-content/<int:pk>/', views.update_content, name='update-content'),
    path('list-content/', views.list_content, name='list-content'),
]
