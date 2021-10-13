from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Name={self.username},email={self.email}'


class Cart(models.Model):
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return f"customer=<{self.customer}>"


class Product(models.Model):
    goods = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    price = models.FloatField()
    carts = models.ManyToManyField(Cart)

    def __str__(self):
        return f"goods=<{self.goods}>,price=<{self.price}>"
