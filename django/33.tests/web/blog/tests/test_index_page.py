from django.test import TestCase
from django.contrib.auth import get_user_model

class TestIndexPage(TestCase):
    """
    Запросы к index_page
    """
    def setUp(self):
        self.user_data = {'username': 'test', 'password': 'password'}
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_status_code(self):
        """Проверяется что код ответа - 200"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_anonymous_user(self):
        """
        Проверяется что в контексте анонимный пользователь, и он получает соотвествующее привествие.
        """
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertContains(response, 'Hello, Stranger!')
    
    def test_logged_user(self):
        """
        Проверяется что залогиненный пользователь получает соотвествующее приветствие
        """
        self.client.login(**self.user_data)

        response = self.client.get('/')
        self.assertEqual(response.context['user'], self.user)
        self.assertTrue(response.context['user'].is_authenticated)
        username = response.context['user'].username
        self.assertContains(response, f'Hello, {username}!')
    
    def test_visibility_anonymous_user(self):
        """
        Проверяется что анонимный пользователь видит кнопки LOGIN и REGISTER
        """
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertContains(response, 'LOGIN')
        self.assertContains(response, 'REGISTER')

    def test_visibility_logged_user(self):
        """
        Проверяется что залогиненный пользователь видит LOGOUT
        """
        self.client.login(**self.user_data)
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'LOGOUT')
