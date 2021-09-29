# [Class-based views](https://docs.djangoproject.com/en/3.2/topics/class-based-views/)
Описание.
## TemplateView
Позволяет добавлять статические страницы. Не нужно объявлять вьюху в файле **view.py**.

Требуется только объявить адрес в диспетчере адресов и создать темплейт.

**urls.py**
```python
from django.views.generic import TemplateView
...
path('about/', TemplateView.as_view(template_name='blog/about.html')),
...
```
## ListView
Позволяет перечислить объекты модели:

**models.py**
```python
class Author(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
```

**view.py**
```python
from django.views.generic import ListView
...
class AuthorListView(ListView):
    model = Author
```

**urls.py**
```python
path('', blog.AuthorListView.as_view(),
```

**blog/author_list.html**
```html
<body>
{% for author in object_list %}
  <p> Name -> {{ author.name }}, email -> {{ author.email }}</p>
{% endfor %}
</body>
```
