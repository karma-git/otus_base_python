from django.test import TestCase
from django.contrib.auth import get_user_model
from django import forms
from store.models import User, Product


class ProductModelTest(TestCase):
    """
    Тестируется модель продукта
    """
    def setUp(self):
        self.product_data = {'goods': 'Google Pixel 4a', 'description': 'экран: 5.8" (2340×1080)...', 'price': 36_990}
        self.product = Product.objects.create(**self.product_data)
    
    def tearDown(self):
        """
        meaningless method
        """
        del self.product

    def test_products_len(self):
        """
        Проверяется количество продуктов
        """
        qty = Product.objects.count()
        self.assertEqual(qty, 1)
    
    def test_products_name(self):
        """
        Проверяется количество продуктов
        """
        name = Product.objects.get(id=1).goods
        self.assertEqual(name, self.product.goods)
