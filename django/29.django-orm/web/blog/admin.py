from django.contrib import admin
from blog.models import (
    Author,
    Articles,
    Tags,
)

# Register your models here.

admin.site.register(Author)
admin.site.register(Articles)
admin.site.register(Tags)
