from rest_framework.test import APITestCase
from user.models import User
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

        # Save the token for authorization ussage and returning user id
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return response.data["id"]

    def test_get_all_items(self):
        """Is a unit test to check if the REST GET call is working to return all stored users"""
        # arrange
        self.authenticate()

        # act
        response = self.client.get(reverse("user"))

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_one_user_by_id(self):
        """Is a unit test to check if the REST GET call is working to return the provided user id info"""
        # arrange
        user_id = self.authenticate()

        # act
        response = self.client.get(f"/user/?id={user_id}")

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_info(self):
        """Is a unit test to check if the REST PUT call is working to update the provided user id info"""
        # arrange
        test_updated_data = {
            "username": "testupdateduser",
            "email": "test@email.test",
            "password": "testpassword123",
        }
        user_id = self.authenticate()

        # act
        response = self.client.put(f"/user/?id={user_id}", test_updated_data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], test_updated_data["username"])

    def test_update_user_error_when_updated_with_bad_request_data(self):
        """Is a unit test to check the error status code when given user data to update don't pass the serializer parameters"""
        # arrange
        test_updated_data = {"email": "test@email.test", "password": "testpassword123"}
        user_id = self.authenticate()

        # act
        response = self.client.put(f"/user/?id={user_id}", test_updated_data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user(self):
        """Is a unit test to check if the REST DELETE call is working to delete the given user id info"""
        user_id = self.authenticate()
        response = self.client.delete(f"/user/?id={user_id}")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
