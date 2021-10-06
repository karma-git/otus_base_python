from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Name={self.username},email={self.email}'

class Article(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors')

    def __str__(self):
        return f'Title={self.title},author={self.author}'

class Tag(models.Model):
    name = models.CharField(max_length=64)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return f'Name={self.name}'
