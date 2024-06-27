# Humster

Сервис Хомяк (Humster) предоставляет следущие интерфейсы REST API:

* Загрузить файл
* Получить данные ранее загруженного файла
* Получить список ранее загруженных файлов
* Удалить ранее загруженный файл

Реализован на языке Python с использованием framework FastAPI

* [FastAPI](https://fastapi.tiangolo.com/)
* [Status Codes](https://fastapi.tiangolo.com/reference/status)
* [Github FastAPI](https://github.com/tiangolo/fastapi)
* [Unicorn](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)


## Запуск

### Локально

1. Установить зависимости

```
$ pip install --no-cache-dir --upgrade -r ./requirements.txt
```

2. Запустить тесты

```
$ pytest ./api.py
```

3. Запустить сервис

```
$ fastapi dev api.py
```

### Docker-образ


1. Создать Docker-образ

```
$ docker build -t hamster:0.0.1 .
```

2. Запуск Docker-контейнера

```
$ docker run -d --name hamster-container -p 8000:80 hamster:0.0.1
```

## API

Документация по методам API в формате swagger, доступен в браузере, после запуска, по адресу http://localhost:8000/docs

1. Загрузить файл

```
$ curl -v -i -X POST -H "Content-Type: multipart/form-data" -F "file=@text.txt"  http://localhost:8000/
```

2. Получить массив загруженных файлов

```
$ curl -v http://localhost:8000/
```

3. Получить данные загруженного файла

```
$ curl -v http://localhost:8000/test.txt
```

4. Удалить файл

```
$ curl -v -i -X DELETE http://localhost:8000/test.txt
```

