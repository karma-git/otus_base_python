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
## CreateView + dynamic urls
Создаем вьюху (предлагает заполнить все поля из модели Author, и при успехе перенаправляет на главную страницу).
```python
class AuthorCreate(CreateView):
    model = Author
    success_url = '/'
    fields = '__all__'

```
**urls.py**
```python
path('author/create/', blog.AuthorCreate.as_view(), name='author_create'),
```
Используем ***author_create*** как алиас для урла:

**author_list.html**
```html
...
<a href="{% url 'author_create' %}">Create</a>
```
**author_form.html**
```html
<body>
    <h1>New author</h1>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="save">
    </form>
</body>
```
## UpdateView + dynamic urls
Во вьюхе возвращаем колбэк нужной страницы.

**view.py**
```python
from django.urls import reverse_lazy
...
class AuthorUpdate(UpdateView):
    model = Author
    success_url = reverse_lazy('main_page')
    fields = '__all__'
```
**urls.py**
```python
path('author/update/<int:pk>/', blog.AuthorUpdate.as_view(), name='author_update'),
```

**author_list.html**
```html
...
<body>
  <h1>Authors</h1>
  <ul>
    {% for author in object_list %}
      <p> Name -> {{ author.name }}, email -> {{ author.email }}</p>
      <p><a href="{% url 'author_update' author.pk %}">edit</a></p>
    {% endfor %}
  </ul>
  <a href="{% url 'author_create' %}">Create</a>
</body>
```
