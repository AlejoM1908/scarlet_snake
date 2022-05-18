from rest_framework.test import APITestCase
from user.models import User
from django.urls import reverse
from rest_framework import status

class TestModel(APITestCase):
    def authenticate(self):
        auth_data = {'username':'testuser', 'email': 'test@email.test', 'password': 'testpassword123'}

        self.client.post(reverse('register'), auth_data)
        response = self.client.post(reverse('auth'), auth_data)
        token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return response.data['id']

    def test_get_all_items(self):
        self.authenticate()
        response = self.client.get(reverse('user'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_one_user_by_id(self):
        user_id = self.authenticate()
        response = self.client.get(f'/user/?id={user_id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_info(self):
        test_updated_data = {'username':'testupdateduser', 'email': 'test@email.test', 'password': 'testpassword123'}

        user_id = self.authenticate()
        response = self.client.put(f'/user/?id={user_id}', test_updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], test_updated_data['username'])

    def test_update_user_error_when_updated_with_bad_request_data(self):
        test_updated_data = {'email': 'test@email.test', 'password': 'testpassword123'}

        user_id = self.authenticate()
        response = self.client.put(f'/user/?id={user_id}', test_updated_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user(self):
        user_id = self.authenticate()
        response = self.client.delete(f'/user/?id={user_id}')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)