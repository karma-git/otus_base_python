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

Links:
- [docs.django](https://docs.djangoproject.com/en/3.2/intro/tutorial05/#create-a-test-to-expose-the-bug) - Create a test to expose the bug

https://realpython.com/testing-in-django-part-1-best-practices-and-examples/

https://realpython.com/testing-in-django-part-2-model-mommy-vs-django-testing-fixtures/

https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Testing

# Тесты:

- IndexPage
- Auth
- LoginRequired
- Permissions

## Coverage
```bash
coverage run manage.py test blog -v 2
coverage html
```
В фолдере с менеджмент скриптом соберется coverage репорт.
