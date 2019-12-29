from rest_framework import serializers

from .. import models


class ProgramInformationsSerializer(serializers.ModelSerializer):
    classes = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = models.Program
        fields = (
            'name', 'classes',
            'students' 
        )

    def get_classes(self, obj):
        return obj.classes.count()

    def get_students(self, obj):
        classes = obj.classes.all()
        students = models.Student.objects.filter(class_id__in=classes)
        return students.count()


class ClassInformationsSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = models.Program
        fields = (
            'name', 'courses',
            'students' 
        )

    def get_courses(self, obj):
        return obj.courses.count()

    def get_students(self, obj):
        return obj.students.count()
