# Схема
Создаем модели для следующей схемы:

![schema](/practise/django/2.django-query-debugtoolbar/docs/db_schema.jpeg)

## Запросы
Заходим в django shell и импортируем модели:
```bash
$ python3 manage.py shell
Python 3.7.9 (v3.7.9:13c94747c7, Aug 15 2020, 01:31:08)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from blog.models import Author, Articles, Tags
```
Запрос `SELECT * FROM table;` - возвращает объект типа **QuerySet**
```bash
>>> authors = Author.objects.all()
>>> authors
<QuerySet [<Author: Name=Mason Cole,email=mason@gmail.com>, <Author: Name=Gavrila Hall,email=gavrila@gmail.com>, <Author: Name=Daveth Tóni,email=daveth@gmail.com>]>
```
Объект типа QuerySet имеет атрибут **.query** который выводит сырой запрос (нужно обернуть в print() иди str() )

Т.к. это коллекция, то можно использовать слайсы, которыt под капотом являются offset и limit.
```sql
SELECT "blog_author"."id", "blog_author"."name", "blog_author"."email" FROM "blog_author"
```
### .only() == WHERE
```bash
>>> authors = Author.objects.only('name').all()
>>> authors[0]
<Author: Name=Mason Cole,email=mason@gmail.com>
```
Если сделать так:
```bash
>>> authors[0].email
'mason@gmail.com'
```
То джанго сгоняет в базу, и вытащит поле email с помощью доп запроса. А в примере ниже - в одном запросе.

```bash
>>> authors = Author.objects.only('name', 'email').all()
>>> authors[0].email
'mason@gmail.com'
```
Only - нужно иметь ввиду, что через онли можно породить много потенциально лишних запросов, в случае если потребуется обратиться к полю которого не было в only.

Можно сделать нормализацию, сделать one-to-one с другой таблицей, в которой будет тяжелое поле.
### Запрос к атрибуту связанной таблицы:
```bash
>>> posts = Articles.objects.only('title').first() # -> Возвращает уже не QuerySet
>>> type(posts)
<class 'blog.models.Articles'>
>>> posts
<Articles: Title=ubuntu 18.04,author=Name=Daveth Tóni,email=daveth@gmail.com>
>>> posts.author.email
'daveth@gmail.com'
```
### Filter
```bash
>>> posts = Articles.objects.filter(title='k8s').first().author.email # <- filter не вызывает запрос, а только формирует, но метод first сразу вытаскивает объект из БД
>>> posts
'gavrila@gmail.com'
```
### Get
```bash
>>> posts = Articles.objects.get(id=14).author.email
>>> posts
'gavrila@gmail.com'
```
### Filter vs Get
**filter** - ленивый запрос и может вернуть пустой объект QuerySet

**get** - сразу выполняет запрос и пытается вернуть **уникальный** объект. Возвращает ошибку если не нашел ничего, или нашел более одного объекта.

```bash
>>> posts = Articles.objects.filter(id=17)
>>> posts
<QuerySet []>
>>> posts = Articles.objects.get(id=17)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/Users/a.horbach/repository-self/python/otus_base_python/practise/django/2.django-query-debugtoolbar/venv/lib/python3.7/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Users/a.horbach/repository-self/python/otus_base_python/practise/django/2.django-query-debugtoolbar/venv/lib/python3.7/site-packages/django/db/models/query.py", line 431, in get
    self.model._meta.object_name
blog.models.Articles.DoesNotExist: Articles matching query does not exist.
```
### Exclude
```bash
>>> authors = Author.objects.exclude(email='mason@gmail.com')
>>> authors
<QuerySet [<Author: Name=Gavrila Hall,email=gavrila@gmail.com>, <Author: Name=Daveth Tóni,email=daveth@gmail.com>]>
```
-> OR, иногда нужно писать пару эксклудов
```bash
>>> authors = Author.objects.exclude(email='mason@gmail.com').exclude(name='Masoc Cole')
>>> authors
<QuerySet [<Author: Name=Gavrila Hall,email=gavrila@gmail.com>, <Author: Name=Daveth Tóni,email=daveth@gmail.com>]>
```
-> AND
```.exclude(name='author', email='his_email')```
### Count
```bash
>>> articles_qty = Articles.objects.count()
>>> articles_qty
9
```
### suffix
**.filter()**
```
qty__gt    --- greater then >
gte        --- greater then or equal >=
lt         --- <
lte        --- <==
contains   --- есть ли слово в 
startswith ---
like       ---
ilike      ---
```
### Найти все посты определенного автора  <**SELECT-RELATED**>
Через таблицу **Articles**
```bash
>>> mason = Author.objects.filter(name__contains='Mason').first()
>>> mason
<Author: Name=Mason Cole,email=mason@gmail.com>
>>> mason_articles = Articles.objects.filter(author_id=mason.id)
>>> mason_articles
<QuerySet [<Articles: Title=Vue.js,author=Name=Mason Cole,email=mason@gmail.com>, <Articles: Title=Node.js,author=Name=Mason Cole,email=mason@gmail.com>, <Articles: Title=Django (web framework),author=Name=Mason Cole,email=mason@gmail.com>, <Articles: Title=FastAPI,author=Name=Mason Cole,email=mason@gmail.com>]>
```
Через таблицу **Author**
```bash
>>> posts = mason.authors.all()
>>> posts
<QuerySet [<Articles: Title=Vue.js,author=Name=Mason Cole,email=mason@gmail.com>, <Articles: Title=Node.js,author=Name=Mason Cole,email=mason@gmail.com>, <Articles: Title=Django (web framework),author=Name=Mason Cole,email=mason@gmail.com>, <Articles: Title=FastAPI,author=Name=Mason Cole,email=mason@gmail.com>]>
```
```sql
>>> str(posts.query)
'SELECT "blog_articles"."id", "blog_articles"."title", "blog_articles"."text", "blog_articles"."author_id" FROM "blog_articles" WHERE "blog_articles"."author_id" = 4'
```
Важно понимать следующий момент, мы указываем **authors** т.к. это у нас указано как позиционный аргумент в модели:
```python
class Author(models.Model):
...

class Articles(models.Model):
...
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authors')
...
```

Если бы related_name не было указано, то запрос строился бы как (`<имя_модели>_set`):
```bash
>>> posts = mason.articles_set.all()
```

!! **related_name** в рамках модели должны быть уникальными
### Select many-to-many
```bash
>>> linux_posts = Articles.objects.filter(tags__name='linux')
>>> linux_posts
<QuerySet [<Articles: Title=ubuntu 18.04,author=Name=Daveth Tóni,email=daveth@gmail.com>, <Articles: Title=Django (web framework),author=Name=Mason Cole,email=mason@gmail.com>]>
```
```sql
'SELECT "blog_articles"."id", "blog_articles"."title", "blog_articles"."text", "blog_articles"."author_id" FROM "blog_articles" INNER JOIN "blog_tags_articles" ON ("blog_articles"."id" = "blog_tags_articles"."articles_id") INNER JOIN "blog_tags" ON ("blog_tags_articles"."tags_id" = "blog_tags"."id") WHERE "blog_tags"."name" = linux'
```
---
```bash
>>> posts_author = Articles.objects.select_related('author').filter(author__name__contains='Mason').all()
>>> posts_author
<QuerySet [<Articles: Title=Vue.js,author=Name=Mason Cole,email=mason@gmail.com>, <Articles: Title=Node.js,author=Name=Mason Cole,email=mason@gmail.com>, <Articles: Title=Django (web framework),author=Name=Mason Cole,email=mason@gmail.com>, <Articles: Title=FastAPI,author=Name=Mason Cole,email=mason@gmail.com>]>
```
```sql
>>> str(posts_author.query)
'SELECT "blog_articles"."id", "blog_articles"."title", "blog_articles"."text", "blog_articles"."author_id", "blog_author"."id", "blog_author"."name", "blog_author"."email" FROM "blog_articles" INNER JOIN "blog_author" ON ("blog_articles"."author_id" = "blog_author"."id") WHERE "blog_author"."name" LIKE %Mason% ESCAPE \'\\\''
```
Как добавить? 26:00
### prefetch_related - M2M - python
Кэшируется на уровня пайтона
## DEBUG tool bar
https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
```bash
ip install django-debug-toolbar
```
**settings.py**
```python
INSTALLED_APPS = [
# ...
    'debug_toolbar',
]
...
MIDDLEWARE = [
#...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
...
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _: True,
}

```
**urls.py**
```python
...
from django.urls import path, include
from web.settings import DEBUG
...
urlpatterns = [
...
]

if DEBUG:
    import debug_toolbar

    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)),)
```
### SQL django-toolbar
Помогает оптимизировать SQL запросы:

**view.py**
```python
def root(request):
    authors = Author.objects.only('name').all()
    return render(request, 'blog/index.html', {'authors': authors})
```
**index.html**
```html
<body>
{% for author in authors %}
  <p> Name -> {{ author.name }}, email -> {{ author.email }}</p>
{% endfor %}
</body>
```
Результат: 

![schema](/practise/django/2.django-query-debugtoolbar/docs/bad_query.png)

---
Правильно:

**view.py**
```python
def root(request):
    authors = Author.objects.all()
    return render(request, 'blog/index.html', {'authors': authors})
```

![schema](/practise/django/2.django-query-debugtoolbar/docs/good_query.png)
### prefetch_related
#### Плохо
**views.py**
```python
def check_tags(request):
    tags = Tags.objects.all()
    return render(request, 'blog/tags.html', {'tags': tags})
```
**template**
```html
<body>
<ul>
    {% for tag in tags %}
      <li>{{ tag.name }}</li>
      <ul>
          {% for article in tag.articles.all %}
            <li>{{ article.title }}</li>
          {% endfor %}
      </ul>
    {% endfor %}
</ul>
</body>
```
![bad](/practise/django/2.django-query-debugtoolbar/docs/prefetch_related_bad_query.png)
#### Хорошо
**views.py**
```python
def check_tags(request):
    tags = Tags.objects.prefetch_related('articles').all()
    return render(request, 'blog/tags.html', {'tags': tags})
```
![good](/practise/django/2.django-query-debugtoolbar/docs/prefetch_related_good_query.png)
