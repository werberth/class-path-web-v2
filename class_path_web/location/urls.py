from django.urls import path

from . import views


urlpatterns = [
    path('create-location/', views.create_location, name='create-location'),
    path('list-location/', views.list_location, name='list-location'),
]
