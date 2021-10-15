### Домашнее задание "GitHub Actions"
#### Задача:
- добавить GitHub Action с выполнением тестов (можно настроить на выполнение имеющихся тестов, например, тестов Django приложения)
- БОНУС: применить какой-либо открытый ресурс для тестирования и проверки покрытия: Travis, codecov, coveralls и тд
#### Критерии оценки:
- создан GitHub Action с выполнением тестов
---
### Overview

Добавлен [пайплайн](https://github.com/karma-git/otus_base_python/blob/PythonBasic.2021-05/.github/workflows/hw_10.yml).

Включает две джобы: тесты джанго, и pytest с анализом отчета от `codecov`.

#### Codecov

Логинимся на [codecov](https://about.codecov.io/) с помощью gh аккаунта.

Выбираем интересующий нас репозиторий, копируем токен.

В репозитории gh создаем секрет `CODECOV_TOKEN` со значением с codecov.

Делаем пайплайн на основе [примера](https://github.com/marketplace/actions/codecov).

#### Badge

[![codecov](https://codecov.io/gh/karma-git/otus_base_python/branch/PythonBasic.2021-05/graph/badge.svg?token=G6ADPNLRCF)](https://codecov.io/gh/karma-git/otus_base_python)

[Документация](https://docs.codecov.com/docs/status-badges).

При необходимости поменять `target_branch` в ссылке на бэйдж (например у меня актуальная ветка для домашек - `PythonBasic.2021-05`).
