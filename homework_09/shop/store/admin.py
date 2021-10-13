from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import (
    User,
    Cart,
    Product,
)

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Cart)
admin.site.register(Product)
