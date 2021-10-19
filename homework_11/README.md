### Домашнее задание "Gitlab pipelines"
#### Задача:
- создать pipeline с тестированием
- запускать pipeline автоматически в master ветке
- запускать pipeline вручную в MR
#### Критерии оценки:
- создан pipeline с тестированием
- pipeline запускается автоматически в master ветке
- pipeline запускается вручную в MR
---
### GitLab Project

[HW11](https://gitlab.com/otus_base_python/homework_11)

#### GitFlow

При коммите в открытый MR выполняются:
- линтинг
- интеграционные и юнит тесты
- попытка сборки докер образа

При слиянии MR-а с мастером в DH пушится образ с хэшем коммита.

При пуше тэга происходит ретег образа из DH, публикуется образ с тэгом коммита, так же образ пушится в реджистри Heroku.

Публикация новой версии приложения в Heroku - мануальная джоба.

#### Требования

Для job связанных с Heroku реджистри требуется доступ к докер сокету, поэтому они запускаются на собственном раннере.

Требуются следующие CI/CD переменные:
- DOCKER_USER
- DOCKER_TOKEN
- HEROKU_API_KEY

#### Результат
- [MR](https://gitlab.com/otus_base_python/homework_11/-/merge_requests/1)
- [пайплайн MR-а](https://gitlab.com/otus_base_python/homework_11/-/pipelines/390865015)
- [пайплайн](https://gitlab.com/otus_base_python/homework_11/-/pipelines/390866381) мерджа MR-а с мастером()
- [пайплайн тэга](https://gitlab.com/otus_base_python/homework_11/-/pipelines/390867096)
- [DH репозиторий](https://hub.docker.com/repository/docker/karmawow/fastapi)
- [Heroku app](https://otus-hw-12.herokuapp.com/)

```bash
$ http https://otus-hw-12.herokuapp.com/isalive
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 15
Content-Type: application/json
Date: Tue, 19 Oct 2021 08:16:58 GMT
Server: uvicorn
Via: 1.1 vegur

{
    "status": "OK"
}

$ http https://otus-hw-12.herokuapp.com/version
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 144
Content-Type: application/json
Date: Tue, 19 Oct 2021 08:16:45 GMT
Server: uvicorn
Via: 1.1 vegur

{
    "commitAuthor": "Andrei Horbach <andrewhorbach@gmail.com>",
    "commitShortSHA": "__CI_COMMIT_SHORT_SHA__",
    "gitTag": "1.0.1",
    "pipelineID": "390866381"
}

$ http https://otus-hw-12.herokuapp.com/
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 138
Content-Type: application/json
Date: Tue, 19 Oct 2021 08:17:11 GMT
Server: uvicorn
Via: 1.1 vegur

{
    "hostname": "177acfe9-4723-434e-84ce-cc04ac2233f2",
    "timestamp": "2021-10-19T08:17:11.274585",
    "uuid": "36030c72-87a6-4b8c-a8f0-1ca5ef0d21f9"
}
```
