# Hamster
#
# VERSION 0.0.1

FROM python:3.9

MAINTAINER Andrew Sizikov <a.rootcom@gmail.com>

LABEL Version="0.0.1"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api.py /code/

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
