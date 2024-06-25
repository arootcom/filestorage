# Humster

Сервис Хомяк (Humster), принимает и отображает уже загруженные файлы.

Используем Python FastAPI

* [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* [https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)

## Подготовка к запуску

```
$ pip install fastapi
$ pip install python-multipart
```

## Тестирование

```
$ pip install pytest
```

```
```

## Запуск

```
$ fastapi dev api.py
```

## Загрузить файл

```
$ curl -v -i -X POST -H "Content-Type: multipart/form-data" -F "file=@text.txt"  http://localhost:8000/
```

## Получить массив загруженных файлов

```
$ curl -v http://localhost:8000/
```
