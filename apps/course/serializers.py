from rest_framework import serializers
from course.models import Course


class CourseSerializer(serializers.ModelSerializer):
    """Used to serialize the data provided in a HTTP request as a Course model"""

    class Meta:
        model = Course
        fields = ("id", "name", "description", "created_at")
