from rest_framework import generics, permissions

from .. import models
from . import serializers


class ProgramInformationsView(generics.RetrieveAPIView):
    model = models.Program
    serializer_class = serializers.ProgramInformationsSerializer
    authentication_classes = [permissions.IsAuthenticated]


class ClassInformationsView(generics.RetrieveAPIView):
    model = models.Class
    serializer_class = serializers.ClassInformationsSerializer
    authentication_classes = [permissions.IsAuthenticated]


# generics as CBVs
program_informations = ProgramInformationsView.as_view()
class_informations = ClassInformationsView.as_view()
