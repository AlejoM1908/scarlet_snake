from rest_framework import serializers
from homework.models import Homework, Submition

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ('id', 'cs_id', 'name', 'description', 'limit_date')

class SubmitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submition
        fields = ('id', 'hw_id', 'data')