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

    def test_course_not_created_without_user_auth(self):
        """Is a unit test to check that the user has to be authorized"""
        # arrange and act
        previus_count = Course.objects.all().count()
        test_data = {"name": "test course", "description": "test description"}
        response = self.client.post(reverse("course"), test_data)
        new_count = Course.objects.all().count()

        # assert
        self.assertEqual(previus_count, new_count)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_created_with_user_auth(self):
        """Is a unit test to check the creation of a course when user has authorization"""
        # arrange and act
        previus_count = Course.objects.all().count()
        test_data = {"name": "test course", "description": "test description"}
        self.authenticate()
        response = self.client.post(reverse("course"), test_data)
        new_count = Course.objects.all().count()

        # assert
        self.assertEqual(previus_count + 1, new_count)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], test_data["name"])
        self.assertEqual(response.data["description"], test_data["description"])

    def test_error_when_course_created_with_bad_request_data(self):
        """Is a unit test to check the error status when request data is incorrect and the user has authorization"""
        # arrange and act
        previus_count = Course.objects.all().count()
        test_data = {"description": "test description"}
        self.authenticate()
        response = self.client.post(reverse("course"), test_data)
        new_count = Course.objects.all().count()

        # assert
        self.assertEqual(previus_count, new_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_items(self):
        """Is a unit test to check if the REST GET call is working to return all the stored courses created by the user"""
        # arrange
        test_data = {"name": "test course", "description": "test description"}
        self.authenticate()

        # act
        self.client.post(reverse("course"), test_data)
        response = self.client.get(reverse("course"))

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_one_course_by_id(self):
        """Is a unit test to check if the REST GET call is working to return the provided couse info"""
        # arrange
        test_data = {"name": "test course", "description": "test description"}
        self.authenticate()

        # act
        course_id = self.client.post(reverse("course"), test_data)
        course_id = course_id.data["id"]
        response = self.client.get(f"/course/?id={course_id}")

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course_info(self):
        """Ia a unit test to check if the REST PUT call is working to update the provided course info"""
        # arrange
        test_data = {"name": "test course", "description": "test description"}
        test_updated_data = {
            "name": "test course updated",
            "description": "test description updated",
        }
        self.authenticate()

        # act
        course_id = self.client.post(reverse("course"), test_data)
        course_id = course_id.data["id"]
        response = self.client.put(f"/course/?id={course_id}", test_updated_data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], test_updated_data["name"])
        self.assertEqual(response.data["description"], test_updated_data["description"])

    def test_update_course_error_when_updated_with_bad_request_data(self):
        """Is a unit test to check the error status code when the given course data to update don't pass the serializer parameters"""
        # arrange
        test_data = {"name": "test course", "description": "test description"}
        test_updated_data = {"description": "test description updated"}
        self.authenticate()

        # act
        course_id = self.client.post(reverse("course"), test_data)
        course_id = course_id.data["id"]
        response = self.client.put(f"/course/?id={course_id}", test_updated_data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_course(self):
        """Is a unit test to check if the REST DELETE call is working to delete the given course id info"""
        # arrange
        test_data = {"name": "test course", "description": "test description"}
        self.authenticate()

        # act
        course_id = self.client.post(reverse("course"), test_data)
        course_id = course_id.data["id"]
        response = self.client.delete(f"/course/?id={course_id}")

        # assert
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
