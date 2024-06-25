# Humster

Сервис Хомяк (Humster), принимает и отображает уже загруженные файлы.

Используем Python FastAPI

* [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* [https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)

```
$ pip install fastapi
$ pip install python-multipart
```

```
$ fastapi dev api.py
```

```
$ curl -v -i -X POST -H "Content-Type: multipart/form-data" -F "file=@README.md"  http://localhost:8000/
```

```
$ curl -v http://localhost:8000/
```
