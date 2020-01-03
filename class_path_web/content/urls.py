from django.urls import path

from . import views


urlpatterns = [
    path('create-content/', views.create_content, name='create-content'),
    path('create-activity/', views.create_activity, name='create-activity'),
    path('update-content/<int:pk>/', views.update_content, name='update-content'),
    path('delete-content/<int:pk>/', views.delete_content, name='delete-content'),
    path('list-content/', views.list_content, name='list-content'),
]
