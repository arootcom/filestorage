import os
import mimetypes

from fastapi import FastAPI, UploadFile, Response, status
from fastapi.testclient import TestClient
from fastapi.responses import FileResponse

files_dir = "/tmp/files"

if not os.path.isdir(files_dir):
    os.mkdir(files_dir)

app = FastAPI()

#
# Если файл слишком большой, чтобы поместиться в памяти — например, если у вас 8 ГБ оперативной памяти,
# вы не сможете загрузить файл объемом 50 ГБ (не говоря уже о том, что доступная оперативная память всегда
# будет меньше общего объема, установленного на вашем компьютере, как и у других приложений будет
# использоваться часть оперативной памяти) — вам лучше загружать файл в память по частям и обрабатывать
# данные по одному фрагменту за раз. Однако выполнение этого метода может занять больше времени,
# в зависимости от выбранного вами размера блока — в приведенном ниже примере размер блока
# составляет 1024 * 1024 байта (т.е. 1 МБ). Вы можете настроить размер фрагмента по своему желанию.
#

@app.post("/")
async def create_upload_file(file: UploadFile, response: Response):
    filename = files_dir + "/" + file.filename
    try:
        with open(filename, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    response.status_code = status.HTTP_201_CREATED
    return {"message": f"Successfully uploaded {file.filename}"}

#

@app.get("/")
async def files():
    files = os.listdir(files_dir)
    return {"files": files}

#

@app.get("/{file_path:path}")
async def read_file(file_path: str, response: Response):
    filename = files_dir + "/" + file_path
    if os.path.isfile(filename):
        return FileResponse(filename)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"File {file_path} not found"}

#
# Тесты
#

client = TestClient(app)

def test_post():
    with open("./test.txt", "rb") as file:
        response = client.post("/", files={"file": ("test.txt", file, "text/plain")})
        assert response.status_code == 201
        assert response.json() == {"message": "Successfully uploaded test.txt"}

def test_get_files():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"files": ["test.txt"]}

def test_file_not_found():
    response = client.get("/test2.txt")
    assert response.status_code == 404
    assert response.json() == {'message': 'File test2.txt not found'}

def test_get_file():
    response = client.get("/test.txt")
    assert response.status_code == 200
    assert response.text == "This`is test file\nNext string.\n"
