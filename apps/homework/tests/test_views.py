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

    def test_homework_not_created_without_user_auth(self):
        previus_count = Homework.objects.all().count()
        course_id = self.create_course()
        self.client.credentials(HTTP_AUTHORIZATION='')
        test_data = {'cs_id': course_id, 'name': 'test homework', 'description': 'test description', 'limit_date':'2025-08-19 16:00:00'}

        response = self.client.post(reverse('homework'), test_data)
        new_count = Homework.objects.all().count()

        self.assertEqual(previus_count, new_count)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_homework_created_with_user_auth(self):
        previus_count = Homework.objects.all().count()
        course_id = self.create_course()
        test_data = {'cs_id': course_id, 'name': 'test homework', 'description': 'test description', 'limit_date':'2025-08-19 16:00:00'}

        response = self.client.post(reverse('homework'), test_data)
        new_count = Homework.objects.all().count()

        self.assertEqual(previus_count + 1, new_count)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cs_id'], test_data['cs_id'])
        self.assertEqual(response.data['name'], test_data['name'])
        self.assertEqual(response.data['description'], test_data['description'])

    def test_error_when_homework_created_with_bad_request_data(self):
        previus_count = Homework.objects.all().count()
        course_id = self.create_course()
        test_data = {'cs_id': course_id, 'description': 'test description', 'limit_date':'2025-08-19 16:00:00'}

        response = self.client.post(reverse('homework'), test_data)
        new_count = Homework.objects.all().count()

        self.assertEqual(previus_count, new_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_items(self):
        course_id = self.create_course()
        test_data = {'cs_id': course_id, 'name': 'test homework', 'description': 'test description', 'limit_date':'2025-08-19 16:00:00'}

        self.client.post(reverse('homework'), test_data)
        response = self.client.get(reverse('homework'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_one_homework_by_id(self):
        course_id = self.create_course()
        test_data = {'cs_id': course_id, 'name': 'test homework', 'description': 'test description', 'limit_date':'2025-08-19 16:00:00'}

        homework_id = self.client.post(reverse('homework'), test_data)
        homework_id = homework_id.data['id']
        response = self.client.get(f'/homework/?id={homework_id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_homework_info(self):
        course_id = self.create_course()
        test_data = {'cs_id': course_id, 'name': 'test homework', 'description': 'test description', 'limit_date':'2025-08-19 16:00:00'}
        test_updated_data = {'cs_id': course_id, 'name': 'test homework updated', 'description': 'test description updated', 'limit_date':'2025-08-19 16:00:00'}

        homework_id = self.client.post(reverse('homework'), test_data)
        homework_id = homework_id.data['id']
        response = self.client.put(f'/homework/?id={homework_id}', test_updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], test_updated_data['name'])
        self.assertEqual(response.data['description'], test_updated_data['description'])

    def test_update_homework_error_when_updated_with_bad_request_data(self):
        course_id = self.create_course()
        test_data = {'cs_id': course_id, 'name': 'test homework', 'description': 'test description', 'limit_date':'2025-08-19 16:00:00'}
        test_updated_data = {'cs_id': course_id, 'description': 'test description', 'limit_date':'2025-08-19 16:00:00'}

        homework_id = self.client.post(reverse('homework'), test_data)
        homework_id = homework_id.data['id']
        response = self.client.put(f'/homework/?id={homework_id}', test_updated_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_homework(self):
        course_id = self.create_course()
        test_data = {'cs_id': course_id, 'name': 'test homework', 'description': 'test description', 'limit_date':'2025-08-19 16:00:00'}

        self.authenticate()
        homework_id = self.client.post(reverse('homework'), test_data)
        homework_id = homework_id.data['id']
        response = self.client.delete(f'/homework/?id={homework_id}')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)