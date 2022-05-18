from rest_framework.test import APITestCase
from course.models import Course
from django.urls import reverse
from rest_framework import status

class TestModel(APITestCase):
    def authenticate(self):
        auth_data = {'username':'testuser', 'email': 'test@email.test', 'password': 'testpassword123'}

        self.client.post(reverse('register'), auth_data)
        response = self.client.post(reverse('auth'), auth_data)
        token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_course_not_created_without_user_auth(self):
        previus_count = Course.objects.all().count()
        test_data = {'name': 'test course', 'description': 'test description'}

        response = self.client.post(reverse('course'), test_data)
        new_count = Course.objects.all().count()

        self.assertEqual(previus_count, new_count)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_created_with_user_auth(self):
        previus_count = Course.objects.all().count()
        test_data = {'name': 'test course', 'description': 'test description'}

        self.authenticate()
        response = self.client.post(reverse('course'), test_data)
        new_count = Course.objects.all().count()

        self.assertEqual(previus_count + 1, new_count)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], test_data['name'])
        self.assertEqual(response.data['description'], test_data['description'])

    def test_error_when_course_created_with_bad_request_data(self):
        previus_count = Course.objects.all().count()
        test_data = {'description': 'test description'}

        self.authenticate()
        response = self.client.post(reverse('course'), test_data)
        new_count = Course.objects.all().count()

        self.assertEqual(previus_count, new_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_items(self):
        test_data = {'name': 'test course', 'description': 'test description'}

        self.authenticate()
        self.client.post(reverse('course'), test_data)
        response = self.client.get(reverse('course'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_one_course_by_id(self):
        test_data = {'name': 'test course', 'description': 'test description'}

        self.authenticate()
        course_id = self.client.post(reverse('course'), test_data)
        course_id = course_id.data['id']
        response = self.client.get(f'/course/?id={course_id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course_info(self):
        test_data = {'name': 'test course', 'description': 'test description'}
        test_updated_data = {'name': 'test course updated', 'description': 'test description updated'}

        self.authenticate()
        course_id = self.client.post(reverse('course'), test_data)
        course_id = course_id.data['id']
        response = self.client.put(f'/course/?id={course_id}', test_updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], test_updated_data['name'])
        self.assertEqual(response.data['description'], test_updated_data['description'])

    def test_update_course_error_when_updated_with_bad_request_data(self):
        test_data = {'name': 'test course', 'description': 'test description'}
        test_updated_data = {'description': 'test description updated'}

        self.authenticate()
        course_id = self.client.post(reverse('course'), test_data)
        course_id = course_id.data['id']
        response = self.client.put(f'/course/?id={course_id}', test_updated_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_course(self):
        test_data = {'name': 'test course', 'description': 'test description'}

        self.authenticate()
        course_id = self.client.post(reverse('course'), test_data)
        course_id = course_id.data['id']
        response = self.client.delete(f'/course/?id={course_id}')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)