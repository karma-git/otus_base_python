from django.contrib import admin

# Register your models here.
from store.models import (
    Customer,
    Cart,
    Product,
)

# Register your models here.
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Product)
