from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test create new user"""
        email = 'test@abc.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email , email)
        self.assertTrue(user.check_password (password))

    def test_new_user_email_normalized(self):
        email = 'test@ABC.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """creating user with no email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None , 'test123')

    def test_create_new_superuser(self):
        """test create super user"""
        user = get_user_model().objects.create_superuser(
            'test@abc.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
