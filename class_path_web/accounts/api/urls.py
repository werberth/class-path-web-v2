from django.urls import path

from . import viewsets


urlpatterns = [
    path('program-informations', viewsets.program_informations, name='program-informations'),
    path('class-informations', viewsets.class_informations, name='class-informations'),
]
