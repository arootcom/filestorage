# Humster

Сервис Хомяк (Humster) предоставляет следущие интерфейсы REST API:

* Загрузить файл
* Получить данные ранее загруженного файла
* Получить список ранее загруженных файлов
* Удалить ранее загруженный файл

Реализован на языке Python с использованием framework FastAPI

* [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* [Status Codes](https://fastapi.tiangolo.com/reference/status)
* [https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)

## Подготовка к запуску

```
$ pip install fastapi
$ pip install python-multipart
```

## Тестирование

```
$ pip install pytest
$ pip install httpx
```

```
$ pytest ./api.py
```

## Запуск

```
$ fastapi dev api.py
```

Документация по методам API в формате swagger, доступен в браузере, после запуска, по адресу http://localhost:8000/docs


## Загрузить файл

```
$ curl -v -i -X POST -H "Content-Type: multipart/form-data" -F "file=@text.txt"  http://localhost:8000/
```

## Получить массив загруженных файлов

```
$ curl -v http://localhost:8000/
```

## Получить данные загруженного файла

```
$ curl -v http://localhost:8000/test.txt
```

## Удалить файл

```
$ curl -v -i -X DELETE http://localhost:8000/test.txt
```
