from rest_framework.test import APITestCase
from homework.models import Homework
from django.urls import reverse
from rest_framework import status

class TestModel(APITestCase):
    def authenticate(self):
        auth_data = {'username':'testuser', 'email': 'test@email.test', 'password': 'testpassword123'}

        self.client.post(reverse('register'), auth_data)
        response = self.client.post(reverse('auth'), auth_data)
        token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def create_course(self):
        test_data = {'name': 'test course', 'description': 'test description'}

        self.authenticate()
        response = self.client.post(reverse('course'), test_data)
        return response.data['id']

    def test_course_instance_to_str(self):
        self.authenticate()
        course_id = self.create_course()
        test_data = {'cs_id': course_id, 'name': 'test homework', 'description': 'test description', 'limit_date':'2025-08-19 16:00:00'}

        response = self.client.post(reverse('homework'), test_data)
        homework = Homework.objects.get(id= response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(homework), test_data['name'])