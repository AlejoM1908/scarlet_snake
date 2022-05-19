from rest_framework import serializers
from homework.models import Homework, Submition


class HomeworkSerializer(serializers.ModelSerializer):
    """Used to serialize the data provided in a HTTP request as a Homework model"""

    class Meta:
        model = Homework
        fields = ("id", "cs_id", "name", "description", "limit_date")


class SubmitionSerializer(serializers.ModelSerializer):
    """Used to serialize the data provided in a HTTP request as a Submition model"""

    class Meta:
        model = Submition
        fields = ("id", "hw_id", "data")
