from django.urls import path, include

from rest_framework import routers

from . import viewsets

router = routers.SimpleRouter()
router.register(r'user', viewsets.UserViewSet)
router.register(r'profile', viewsets.ProfileViewSet)
router.register(r'address', viewsets.AddressViewSet)
router.register(r'program', viewsets.ProgramViewSet)
router.register(r'class', viewsets.ClassViewSet)
router.register(r'course', viewsets.CourseViewSet)
