from rest_framework.test import APITestCase
from user.models import User


class TestModel(APITestCase):
    """
    This class is used to test the models from the user app in the project
    """

    def test_create_user(self):
        """Is a unit test to check the correct creation of a User model"""
        # arrange and act
        user = User.objects.create_user(
            "testuser", "test@email.test", "testpassword123"
        )

        # assert
        self.assertTrue(not user.is_superuser)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@email.test")
        self.assertEqual(user.username, "testuser")

    def test_create_superuser(self):
        """Is a unit test to check the correct creation of a superuser with User model"""
        # arrange and act
        user = User.objects.create_superuser(
            "testsuperuser", "test@email.test", "testpassword123"
        )

        # assert
        self.assertTrue(user.is_superuser)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@email.test")
        self.assertEqual(user.username, "testsuperuser")

    def test_raises_error_when_no_username_provided_to_user(self):
        """Is a unit test to check the thrown exception when no username is provided"""
        # arrange, act and assert
        with self.assertRaisesMessage(ValueError, "The given username must be set"):
            User.objects.create_user("", "test@email.test", "testpassword123")

    def test_raises_error_when_no_email_provided_to_user(self):
        """Is a unit test to check the thrown exception when no email is provided"""
        # arrange, act and assert
        with self.assertRaisesMessage(ValueError, "The given email must be set"):
            User.objects.create_user("testuser", "", "testpassword123")

    def test_superuser_created_with_staff_status(self):
        """Is a unit test to check the thrown exception when superuser don't have is_staff=True"""
        # arrange, act and assert
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(
                "testsuperuser", "test@email.test", "testpassword123", is_staff=False
            )

    def test_superuser_created_with_superuser_status(self):
        """Is a unit test to check the thrown exception when superuser don't have is_superuser=True"""
        # arrange, act and assert
        with self.assertRaisesMessage(
            ValueError, "Superuser must have is_superuser=True."
        ):
            User.objects.create_superuser(
                "testsuperuser",
                "test@email.test",
                "testpassword123",
                is_superuser=False,
            )

    def test_user_instance_to_str(self):
        """Is a unit test to check that __str__ method is correctly working"""
        # arrange and act
        user = User.objects.create_user(
            "testuser", "test@email.test", "testpassword123"
        )

        # assert
        self.assertEqual(str(user), "testuser")
