from rest_framework.test import APITestCase
from user.models import User

class TestModel(APITestCase):
    def test_create_user(self):
        user = User.objects.create_user('testuser','test@email.test','testpassword123')
        self.assertTrue(not user.is_superuser)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@email.test')
        self.assertEqual(user.username, 'testuser')

    def test_create_superuser(self):
        user = User.objects.create_superuser('testsuperuser','test@email.test','testpassword123')
        self.assertTrue(user.is_superuser)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@email.test')
        self.assertEqual(user.username, 'testsuperuser')

    def test_raises_error_when_no_username_provided_to_user(self):
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            User.objects.create_user('', 'test@email.test', 'testpassword123')

    def test_raises_error_when_no_email_provided_to_user(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user('testuser', '', 'testpassword123')

    def test_superuser_created_with_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser('testsuperuser','test@email.test','testpassword123', is_staff=False)

    def test_superuser_created_with_superuser_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser('testsuperuser','test@email.test','testpassword123', is_superuser=False)

    def test_user_instance_to_str(self):
        user = User.objects.create_user('testuser', 'test@email.test','testpassword123')
        self.assertEqual(str(user), 'testuser')