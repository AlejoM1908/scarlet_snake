from rest_framework import serializers
from user.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Used to serialize the data provided in a HTTP request as an User model"""

    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """Used to serialize the data provided in a HTTP request as an User model for login"""

    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role", "token")
        read_only_fields = ["token"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
