from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=64, unique=True)
    email = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"Name=<{self.name}>,email=<{self.email}>"


class Cart(models.Model):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
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
