from rest_framework.test import APITestCase
from homework.models import Homework
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

    def create_course(self):
        """Used to create a course in the test database and be able to use the id to test other endpoints"""
        test_data = {"name": "test course", "description": "test description"}
        self.authenticate()

        # Save course to database and returning the new id
        response = self.client.post(reverse("course"), test_data)
        return response.data["id"]

    def test_course_instance_to_str(self):
        """Is a unit test to check that __str__ method is correctly working"""
        # arrange
        self.authenticate()
        course_id = self.create_course()
        test_data = {
            "cs_id": course_id,
            "name": "test homework",
            "description": "test description",
            "limit_date": "2025-08-19 16:00:00",
        }

        # act
        response = self.client.post(reverse("homework"), test_data)
        homework = Homework.objects.get(id=response.data["id"])

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(homework), test_data["name"])
