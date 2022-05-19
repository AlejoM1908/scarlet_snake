from rest_framework.test import APITestCase
from course.models import Course
from django.urls import reverse
from rest_framework import status


class TestModel(APITestCase):
    def authenticate(self):
        """Used to create a user in the test database and be able to use token protected endpoints"""
        auth_data = {
            "username": "testuser",
            "email": "test@email.test",
            "password": "testpassword123",
        }

        # Save user to test database
        self.client.post(reverse("register"), auth_data)
        response = self.client.post(reverse("auth"), auth_data)
        token = response.data["token"]

        # Save token for authorization ussage
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_course_instance_to_str(self):
        """Is a unit test to check that __str__ method is correctly working"""
        # arrange
        test_data = {"name": "test course", "description": "test description"}
        self.authenticate()

        # act
        response = self.client.post(reverse("course"), test_data)
        course = Course.objects.get(id=response.data["id"])

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(course), test_data["name"])
