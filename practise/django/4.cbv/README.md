# CBV
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
