# Overview

Пишем тесты к [предыдущей](playground/django/32.auth/README.md) версии блога.

Links:
- [docs.django](https://docs.djangoproject.com/en/3.2/intro/tutorial05/#create-a-test-to-expose-the-bug) - Create a test to expose the bug
- [realpython.com](https://realpython.com/testing-in-django-part-1-best-practices-and-examples/) - Testing in Django (Part 1) – Best Practices and Examples
- [realpython.com](https://realpython.com/testing-in-django-part-2-model-mommy-vs-django-testing-fixtures/) - Testing in Django (Part 2) – Model Mommy vs Django Testing Fixtures
- [developer.mozilla.org](http://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Testing) - Руководство часть 10: Тестирование приложений Django

https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Testing

# Тесты:

- IndexPage
- Auth
- LoginRequired
- Permissions

Запускаются с помощью:

```bash
python manage.py test
```

## Coverage
```bash
coverage run manage.py test blog -v 2
coverage html
```
В фолдере с менеджмент скриптом соберется coverage репорт.
