### Домашнее задание "Django Generics"
#### Задача:
- доработайте своё приложение для отображения моделей на страницах
- добавьте страницы ListView и DetailView
#### Критерии оценки:
- данные отображаются на страницах
- есть кнопка для возвращения к списку
- использованы ListView и DetailView
---

### Сборка
Докерфайл проверен с помощью [hadolint](https://hadolint.github.io/hadolint/) и [trivy config](https://aquasecurity.github.io/trivy/v0.17.0/).

Сборка проекта, создание схемы БД и суперпользователя для админки (пароль указывается в build-args).
```bash
docker build -t otus_hw7:1.0 --build-arg SU_PW=123456 .
```
