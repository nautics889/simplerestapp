from django.conf import settings

settings.configure(DEBUG=True)

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class CreateUserViewTestCase(TestCase):
    def setUp(self):
        """Prepare data for testing. APIClient allows us to simulate clients actions"""
        self.client = APIClient()

        self.sign_up_data = {
            'username': 'foobar',
            'email': 'foobar123@gmail.com',
            'password': 'foobar777'
        }

        #try to create user correctly
        self.response_valid = self.client.post(reverse('create_user'), self.signup_data)

        #try to create account with the same username; "Bad request" expected
        self.response_invalid = self.client.post(reverse('create_user'), self.signup_data)

    def create_user_test(self):
        self.assertEqual(self.response_valid.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response_invalid.status_code, status.HTTP_400_BAD_REQUEST)

