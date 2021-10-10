# Overview

ТЗ:

[Усовершенствовать блог](django/29.django-orm#схема).
- Author теперь наследуется от базового пользователя аутентификации django.
- На главной странице видно username текущего авторизированного пользователя.
- Login/Logout/Registration
- Для просмотра урла Articles - нужно залогиниться (редирект на login).
- Добавляются несколько групп пользователей, права распределяются согласно группам(при попытке выполнить запрещенную операцию - получаем [403](https://developer.mozilla.org/ru/docs/Web/HTTP/Status)):
1. Newbee - RO права на все модели
2. Author - VCUD (View Create Update Delete) на Article (подразумевается, что может делать UD только своих объектов).
3. Moderator - VCUD на Article (модерирует всех авторов).
4. Judge - фул права на сайте.
- Элементы CUD видны только при наличии у пользователя прав выполнять операцию.

## Расширение Пользователя из django.auth

Выбор - Расширение модели пользователя с помощью наследования AbstractUser (полулайтовый метод, делается на старте проекта). 

В связанных моделях ссылаемся на модель пользователя через `settings.AUTH_USER_MODEL`

**models.py**
```python
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

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
```
Подключаем этого пользователя в админке.
```python
#settings.py
...
AUTH_USER_MODEL = 'blog.User'
# admin.py
from django.contrib.auth.admin import UserAdmin
from .models import User
...
admin.site.register(User, UserAdmin)
```
Links:
- [https://testdriven.io/](https://testdriven.io/blog/django-custom-user-model/) - Creating a Custom User Model in Django
- [docs.django](https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model) - Auth. Custom User model
- [https://tproger.ru/](https://tproger.ru/translations/extending-django-user-model/) - Расширение модели пользователя в Django: сравнение нескольких стратегий с примерами кода

## Custom Managment Commands <CMC>
Зачем?

Хочу одной командой создать несколько дефолтных групп пользователей и назначить им определенные права на модели.

Создаю в приложении модуль `management` и etc, в файлике initgroups пишу логику, название файлика == название команды.
```bash
.blog
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── management
│   ├── __init__.py
│   └── commands
│       ├── __init__.py
│       └── initgroups.py
├── models.py
├── templates
├── tests.py
└── views.py
```

Links:
- [docs.django](https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/) CMC
- [coderoad.ru](https://coderoad.ru/22250352/%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%BE-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%B9%D1%82%D0%B5-%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D1%83-django-%D1%81-%D1%80%D0%B0%D0%B7%D1%80%D0%B5%D1%88%D0%B5%D0%BD%D0%B8%D1%8F%D0%BC%D0%B8) - Программно создайте группу django с разрешениями

## Custom Template Tags <CTT>
Зачем?

Хочу отображать html-элемент в зависимости от принадлежности пользователя к какой-либо группе пользователей.

Для это воспользуемся инструментом `CTT` - это просто функция, в которую передается имя группы, и возвращается bool в зависимости от принадлжености пользователя к этой группе.

Структура -> добавляется templatetags и внутри модуля пишется `CTT`.
```bash
.blog
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── management
│   ├── __init__.py
│   └── commands
│       ├── __init__.py
│       └── initgroups.py
├── models.py
├── templates
│   ├── base_generic.html
|   ...
|
├── templatetags
│   ├── __init__.py
│   └── auth_extras.py
├── tests.py
└── views.py
```

custom template tag
```python
# auth_extras.py
from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False
```

Подключаем CTT (можно с помощью `{% load %}`) в `settings.py` (добавляем `'builtins': ['blog.templatetags.auth_extras'],`):
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
               ...
            ],
            'builtins': ['blog.templatetags.auth_extras'],
        },
    },
]
```

Темплейты:
```html
<!-- button_conditionals.html -->
{% if request.user == article.author or request.user|has_group:"Moderator" or request.user|has_group:"Judge" %}
    <div style="margin-top: 35px" id="edit">
    <a href="{{ url_edit }}" class="btn btn-primary" role="button">edit</a>
    <a href="{{ url_delete }}" class="btn btn-primary" role="button">delete</a>
    </div>
{% endif %}
...
<!-- article_detail.html -->
{% url 'article_update' object.id as ue %}
{% url 'article_detail' object.id as ud %}
{% include 'button_conditionals.html' with url_edit=ue url_delete=ud %}
```

Links:
- [docs.django](https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/) - CTT

## PermissionRequiredMixin

Если у полльзователя нет нужных разрешений - он получит 403.

```python
class ArticleDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
     model = Article
     permission_required = 'blog.view_article'
     queryset = Article.objects.only('title', 'text', 'author__username').select_related('author')
```

Links:
- [docs.django](https://docs.djangoproject.com/en/3.2/topics/auth/default/#permissions-and-authorization) - Permissions and Authorization
- [medium.com](https://medium.com/djangotube/django-roles-groups-and-permissions-introduction-a54d1070544) - Django Roles, Groups, and Permissions Introduction
- [realpython.com](https://realpython.com/django-user-management/) - Get Started With Django Part 2: Django User Management

## UserPassesTestMixin

Нужно определить метод `test_func` внутри CBV, который должен возвращать bool. Пользователь будет получать 403 если не пройдет тест.

В данном кейсе создан миксин, который разрешать действие которое будет указано с помощью `PermissionRequiredMixin` для owner-а объекта Article и для пользователей у которых есть группа **"Moderator|Judge"**.


```python
class ArticleTestMixin(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin):
     model = Article
     lookup = 'pk'

     def test_func(self):
          article_author_username = (
               self.model.objects.filter(id=self.kwargs[self.lookup])
               .only('author__username').select_related('author').first()
               .author.username
          )
          current_username = self.request.user.username
          is_author = True if article_author_username == current_username else False
          is_moderator = self.request.user.groups.filter(Q(name='Moderator') | Q(name='Judge')).exists()
          print(is_author, is_moderator)
          return is_author or is_moderator

class ArticleUpdate(ArticleTestMixin, UpdateView):
    ...
```

Links:
- - [docs.django](https://docs.djangoproject.com/en/3.2/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin) - UserPassesTestMixin
- [**raturi.in**]((https://raturi.in/blog/custom-mixins-django-class-based-views/)) - How to create custom mixin in django class based views.
