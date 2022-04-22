FROM python:3.9

RUN mkdir /code

COPY ./docker/application/uwsgi.ini /code/
COPY ./docker/application/requirements.txt /code/

WORKDIR /code

RUN pip install -r requirements.txt

COPY ./src/ /code/

WORKDIR /code/api/

CMD ["uwsgi", "--ini", "/code/uwsgi.ini"]