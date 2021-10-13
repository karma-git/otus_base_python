from django.test import TestCase
from django.contrib.auth import get_user_model
from django import forms
from store.models import User, Product


class TestUserPermissions(TestCase):
    """
    Проверяются доступы
    """

    def setUp(self):
        self.user_data = {"username": "test", "password": "password"}
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_products_page_anonymous_user(self):
        """
        При попытке неавторизованного пользователя перейти по url Products, он получает редирект на login
        """
        response = self.client.get("/")
        self.assertTrue(response.context["user"].is_anonymous)
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 302)

    def test_products_page_logged_user(self):
        """
        Проверяется что залогиненный пользователь попадает на страницу с Products
        """
        self.client.login(**self.user_data)

        response = self.client.get("/")
        self.assertEqual(response.context["user"], self.user)
        self.assertTrue(response.context["user"].is_authenticated)

        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unfortunately, our stock is empty right now.")

    def test_products_page_without_add_permission(self):
        """
        Проверяется что залогиненный пользователь не может добавлять новый продукт
        """
        self.client.login(**self.user_data)
        response = self.client.get("/products/")
        self.assertNotContains(response, "add new product")
        response = self.client.get("/product/create/")
        self.assertEqual(response.status_code, 403)
