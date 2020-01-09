from django.urls import path

from . import views


urlpatterns = [
    path('create-content/', views.create_content, name='create-content'),
    path('create-activity/', views.create_activity, name='create-activity'),
    path('update-content/<int:pk>/', views.update_content, name='update-content'),
    path('update-activity/<int:pk>/', views.update_activity, name='update-activity'),
    path('delete-content/<int:pk>/', views.delete_content, name='delete-content'),
    path('delete-activity/<int:pk>/', views.delete_activity, name='delete-activity'),
    path('list-content/', views.list_content, name='list-content'),
    path('list-activity/', views.list_activity, name='list-activity')
]
