FROM python:3.9

RUN mkdir /code
WORKDIR /code

COPY ./docker/application/requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./src/ /code/