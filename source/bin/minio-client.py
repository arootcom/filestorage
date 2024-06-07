import os

from minio import Minio
from minio.credentials import EnvMinioProvider

os.environ["MINIO_ACCESS_KEY"] = "JHinB0jCTcWNu6qbynGB"
os.environ["MINIO_SECRET_KEY"] = "wZ5u8TggcL49KeYqfrnkF7fBaT2ryFXeTYWLwmR7"

client = Minio("localhost:9000", credentials=EnvMinioProvider(), secure=False)

if client.bucket_exists("my-bucket"):
    print("my-bucket exists")
else:
    print("my-bucket does not exist")

