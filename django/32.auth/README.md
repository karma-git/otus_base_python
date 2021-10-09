# Overview

f8dbc442a5d8ff8efb83146f3ba9a70f497484d8 - создал проект

b451817180e517d0805f4f32964433c90db39078 - добавил тулбар

9cfa7c2474d79e32d999a10c16a4e1ee9aeb1482 - создал Юзера унаследовано от auth.User, он может логиниться в админку

8074f0efac6b4c5593fe62ee609338a4b65f9204 - главная страница, на ней видно имя пользователя

7e81f864c9713cf3de103a8df7e1f4715e6513ae - login/logout

d3fe5673037cb2d97415f115f78954aa05376a57 - форма регистрации, отключение проверки пароля в settings.py

fbbdd32d5c236da9c5228402f6b09f97282897c4 - LoginRequiredMixin

8283b2d6b690b04c42f8dd544163a58a1e24d2cf - Новая команда в manage.py, инициализация новых групп.

189f3624028359953c88ab6a0d775157870d6be0 - Create с помощью PermissionRequierd - при попытки пройти во вьюху без нужных прав получается 403

1c0c32a417ac59c60268043b02d79c08c807979d - Detail view с PermissionRequierd

XXXX - большой коммит

### [Custom Managment Commands <CMC>](https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/)
Зачем?

Хочу одной командой создать несколько дефолтных групп пользователей и назначить им определенные права на модели.

Создаю в приложении модуль `management` и etc, в файлике initgroups пишу логику, название файлика == название команды
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

### [Custom Template Tags <CTT>](https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/)
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

### PermissionRequiredMixin

Если у полльзователя нет нужных разрешений - он получит 403.

```python
class ArticleDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
     model = Article
     permission_required = 'blog.view_article'
     queryset = Article.objects.only('title', 'text', 'author__username').select_related('author')
```

### UserPassesTestMixin

Нужно определить метод `test_func` внутри CBV, который должен возвращать bool. Пользователь будет получать 403 если не пройдет тест.

## TODO
Заставить при создании артикла использовать текущего пользователя!
