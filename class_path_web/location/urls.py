from django.urls import path

from . import views


urlpatterns = [
    path('create-location/', views.create_location, name='create-location'),
    path('update-location/<int:pk>/', views.update_location, name='update-location'),
    path('delete-location/<int:pk>/', views.delete_location, name='delete-location'),
    path('list-location/', views.list_location, name='list-location'),
]
