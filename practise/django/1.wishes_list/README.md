# Getting started with Django
Зачем: чтобы понять абстракции Django и понять иерархическую структуру приложения.
### Установка пакета Django
Все просто, создаем директорию, внутри которой создадим виртуальное окружение и установим Django.
### Создаем проект Django при помощи cli `django admin`
`django-admin startproject wishes_list`

В Результате получим следущую структуру файлов:
```bash
.
├── README.md
├── requirements.txt
└── wishes_list
    ├── db.sqlite3
    ├── manage.py
    └── wishes_list
        ├── __init__.py
        ├── asgi.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

2 directories, 9 files
```

Директория `wishes_list`, в терминалогии инструктора OTUS - называется корнем проекта.
### Создаем Django Application
Создаем `Django Application`, логика выполнения мэнэджмент скрипта через интерпретатор, а не через `django-admin` в том, чтобы находится в директории со скриптом manage.py

`python manage.py startapp gadgets`
```bash                  
$ tree -I venv
.
├── db.sqlite3
├── gadgets
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
└── wishes_list
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

3 directories, 14 files
```
### Регестрируем приложение в `settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    # own apps
    'gadgets',
]
```
### Создаем view ([MVT](https://docs.djangoproject.com/en/dev/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names))
View - это контроллер в моделе [MCV](https://ru.wikipedia.org/wiki/Model-View-Controller)

Вьюха - функция представления, получает запрос, проделывает какую-то логику и отдает ответ.

**FBV** - function base views (views в джанго это контроллер)

**CBV** - class base view

Напишем в файле `./wishes_list/gadgets/views.py` простейшую вьюху которая будет возвращать `None`.

```python
def root(request):
    pass
```

Чтобы вьюха отрабатывала, нужно чтобы запрос который пришел на сайт попал на нее:

Для этого нужно путь на сайте ассоциировать с вьюхой через конфиг `./wishes_list/wishes_list/urls.py`
```python
...
import gadgets.views as gadgets

urlpatterns = [
    path('', gadgets.read_root),

    path('admin/', admin.site.urls),
]
```
Нужно обратить внимание, что вьюха передается как callback обхект, а не callable.

Запустим сервер при помощи команды `python manage.py runserver` и попробуем сделать запрос к ресурсу:
```
ValueError at /
The view gadgets.views.read_root didn't return an HttpResponse object. It returned None instead.
```
### Темплейты

Иерархия в темплейтах следующая
```bash
./wishes_list/gadgets
$ tree
.
└── gadgets
    └── index.html

1 directory, 1 file
```

Создаем html темплейт и редактируем функцию представления:
```python
def read_root(request):
    return render(request, 'gadgets/index.html')
```
### Миграции
Миграция - это превращение классов пайтона в скрипты, которые обновляют схему БД.

Имеет две фазы: 
- создание скрипта миграции (`makemigrations`)
- выполнение скрипта (обновление схемы) - `migrate`

`../wishes_list/gadgets/models.py`

### Добавление записей

#### **экстеншен для VS CODE - sqlite**

[Гитхаб](https://github.com/AlexCovizzi/vscode-sqlite)

[How To на ютубе](https://www.youtube.com/watch?v=bKixKfb1J1o)

#### Django Shell
```bash
# 1. Заходим в шэл
$ python manage.py shell
# 2. Импортируем модуль с моделями
>>> from gadgets.models import Gadget
# 3. Создаем запись в БД
>>> gadget_2 = Gadget.objects.create(name='Magic Mouse', kind='Периферийные устройства', price=9000)
```
### Создать суперюзера (для админки)
```bash
$ python manage.py createsuperuser
```

Чтобы наша модель появилась в админке(`/admin`), и можно было создавать записи в БД нужно в файле `./wishes_list/gadgets/admin.py` зарегать модель:
```python
...
from gadgets.models import Gadget

admin.site.register(Gadget)
```
### Вывод контента БД
#### Изменяем функцию представления
`./wishes_list/gadgets/views.py`
```python
...
from gadgets.models import Gadget

def read_root(request):
    gadgets = Gadget.objects.all()
    return render(request, 
        'gadgets/index.html', 
        context={'gadgets': gadgets})
```
Где ключ словаря, это объект с которым мы будем взаимодйествовать внутри темплейта, а значение это объект полученного в результате запроса к БД через ORM.
#### Изменение темплейта
`./wishes_list/gadgets/templates/gadgets/index.html`
```html
...
 <body>
  <p>Hello world!</p>
  <ul>
      {% for gadget in gadgets %}
        <li>{{ gadget.name }}, and its price -> {{ gadget.price }}</li>
      {% endfor %}
  </ul>
 </body>
 ...
```