from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicApiTest(TestCase):
    """Test the users api public"""


    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user valid payload is successful"""
        payload = {
            'email' : 'abc@gmail.com',
            'password' : 'testpass',
            'name' : 'alireza'
        }

        res = self.client.post(CREATE_USER_URL , payload)

        self.assertEqual(res.status_code , status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password' , res.data)


    def test_user_exist(self):
        """Test user already exists"""
        payload = {
            'email' : 'abc@gmail.com',
            'password' : 'testpass',
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL , payload)

        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)

    def test_pass_too_short(self):
        """test that the pass must be more than 5 char"""
        payload = {
            'email' : 'abc@gmail.com',
            'password' : 'pw',
        }
        res = self.client.post(CREATE_USER_URL , payload)

        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()

        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        print(res.json)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
