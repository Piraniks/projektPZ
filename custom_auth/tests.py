from django.test import TestCase, Client
from django.shortcuts import reverse
from rest_framework import status

from custom_auth.models import User


class RegisterUserTestCase(TestCase):
    def setUp(self):
        client = Client()

    def test_register_page_exists(self):
        response = self.client.get('/register/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_page_redirects_logged_in_user(self):
        username = 'username'
        password = 'password'

        user = User(username=username)
        user.set_password(password)
        user.save()

        self.client.login(username=username, password=password)
        response = self.client.get('/register/')

        self.assertRedirects(response, reverse('index'))

    def test_create_with_valid_data(self):
        username = 'username'
        password = 'password'

        data = {
            'username': username,
            'password': password,
            'password_confirm': password
        }
        response = self.client.post('/register/', data)

        user = User.objects.filter(username=username).first()

        self.assertIsNotNone(user)
        self.assertRedirects(response, reverse('index'))

    def test_create_with_invalid_passwords(self):
        username = 'username'
        password = ''

        data = {
            'username': username,
            'password': password,
            'password_confirm': password
        }
        response = self.client.post('/register/', data)

        user = User.objects.filter(username=username).first()

        self.assertIsNone(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_invalid_username(self):
        username = ''
        password = 'password'

        data = {
            'username': username,
            'password': password,
            'password_confirm': password
        }
        response = self.client.post('/register/', data)

        user = User.objects.filter(username=username).first()

        self.assertIsNone(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_not_matching_passwords(self):
        username = 'username'
        password = 'password'
        other_password = 'other_password'

        data = {
            'username': username,
            'password': password,
            'password_confirm': other_password
        }
        response = self.client.post('/register/', data)

        user = User.objects.filter(username=username).first()

        self.assertIsNone(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_existing_user_username(self):
        username = 'username'
        password = 'password'
        other_password = 'other_password'

        user = User(username=username)
        user.set_password(password)
        user.save()

        self.assertIsNotNone(user)

        data = {
            'username': username,
            'password': other_password,
            'password_confirm': other_password
        }
        response = self.client.post('/register/', data)

        user = User.objects.get(username=username)
        authenticated = self.client.login(username=username, password=password)

        self.assertTrue(authenticated)
        self.assertIsNotNone(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LoginUserTestCase(TestCase):
    def setUp(self):
        client = Client()

    def test_login_page_exists(self):
        response = self.client.get('/login/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_page_redirects_logged_in_user(self):
        username = 'username'
        password = 'password'

        user = User(username=username)
        user.set_password(password)
        user.save()

        self.client.login(username=username, password=password)
        response = self.client.get('/login/')

        self.assertRedirects(response, reverse('index'))

    def test_create_with_invalid_password(self):
        username = 'username'
        password = ''

        user = User(username=username)
        user.set_password(password)
        user.save()

        data = {
            'username': username,
            'password': password
        }
        response = self.client.post('/login/', data)
        response_user = response.context.get('user')

        self.assertTrue(response_user.is_anonymous)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_invalid_username(self):
        username = ''
        password = 'password'

        user = User(username=username)
        user.set_password(password)
        user.save()

        data = {
            'username': username,
            'password': password
        }
        response = self.client.post('/login/', data)
        response_user = response.context.get('user')

        self.assertTrue(response_user.is_anonymous)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_notexisting_user_credentials(self):
        username = 'username'
        password = 'password'

        data = {
            'username': username,
            'password': password
        }
        response = self.client.post('/login/', data)
        response_user = response.context.get('user')

        self.assertTrue(response_user.is_anonymous)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_incorrect_password(self):
        username = 'username'
        password = 'password'
        incorrect_password = 'incorrect_password'

        user = User(username=username)
        user.set_password(password)
        user.save()

        data = {
            'username': username,
            'password': incorrect_password
        }
        response = self.client.post('/login/', data)
        response_user = response.context.get('user')

        self.assertTrue(response_user.is_anonymous)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_valid_data(self):
        username = 'username'
        password = 'password'

        user = User(username=username)
        user.set_password(password)
        user.save()

        data = {
            'username': username,
            'password': password
        }
        response = self.client.post('/login/', data)

        self.assertRedirects(response, reverse('index'))


class LogoutUserTestCase(TestCase):

    def setUp(self):
        client = Client()

    def test_logout_page_redirects_to_main_page(self):
        response = self.client.get('/logout/')

        self.assertRedirects(response, reverse('index'))

    def test_logouts_logged_in_user(self):
        username = 'username'
        password = 'password'

        user = User(username=username)
        user.set_password(password)
        user.save()

        self.client.login(username=username, password=password)
        response = self.client.get('/logout/')

        self.assertRedirects(response, reverse('index'))
