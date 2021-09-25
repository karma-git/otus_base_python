from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=64)
    # FIXME use .EmailField()
    email = models.CharField(max_length=64)

    def __str__(self):
        return f'Name={self.name},email={self.email}'

class Articles(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authors')

    def __str__(self):
        return f'Title={self.title},author={self.author}'

class Tags(models.Model):
    name = models.CharField(max_length=64)
    articles = models.ManyToManyField(Articles)

    def __str__(self):
        return f'Name={self.name}'
