# Rabbitmq
```bash
docker run -d --name some-rabbit -p 5672:5672 -p 5673:5673 -p 15672:15672 rabbitmq:3-management
# OR
docker compose up
```
http://localhost:15672 # login/pw guest/gues 
# [Celery](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html)
**settings.py**
```python
CELERY_BROKER_URL = 'amqp://localhost'
```
**__init__.py** - корень проекта
```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```
**celery.py**
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')  # where as - project name

app = Celery('web', backend='rpc://')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```
На этом этапе можно запустить celery:
```bash
$ celery --app web worker -l INFO
```
# Payload
**blog.task.py**
```python
from celery import shared_task

@shared_task
def do_something():
    pass
```
**view.py**
```python
from blog.tasks import send_email
from celery import current_app
...
    if request.method == "POST":
        task = send_email.delay("Hello from admin", "I am trying celery")
        task_id = task.id
...
```
# explain file backend
**settings.py**
```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages' # change this to a proper location
```
Используется абсолютный путь.
