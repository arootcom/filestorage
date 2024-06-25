import os

from fastapi import FastAPI, UploadFile

filesdir = "/tmp/files"

if not os.path.isdir(filesdir):
    os.mkdir(filesdir)

app = FastAPI()

#
# если файл слишком большой, чтобы поместиться в памяти — например, если у вас 8 ГБ оперативной памяти, 
# вы не сможете загрузить файл объемом 50 ГБ (не говоря уже о том, что доступная оперативная память всегда 
# будет меньше общего объема, установленного на вашем компьютере, как и у других приложений будет 
# использоваться часть оперативной памяти) — вам лучше загружать файл в память по частям и обрабатывать 
# данные по одному фрагменту за раз. Однако выполнение этого метода может занять больше времени, 
# в зависимости от выбранного вами размера блока — в приведенном ниже примере размер блока 
# составляет 1024 * 1024 байта (т.е. 1 МБ). Вы можете настроить размер фрагмента по своему желанию.
#
@app.post("/")
async def create_upload_file(file: UploadFile):
    filename = filesdir + "/" + file.filename
    try:
        with open(filename, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


@app.get("/")
async def files():
    files = os.listdir(filesdir)
    return {"files": files}


