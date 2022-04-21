# CoinAPI

## Docker and OS Setup

1. Install the Docker Client
  - OSX: https://www.docker.com/products/docker-desktop/#/mac
  - Ubuntu
    - docker: https://docs.docker.com/engine/install/ubuntu/
    - docker-compose: https://docs.docker.com/compose/install/
  - Windows: https://www.docker.com/products/docker-desktop/#/windows

## CoinAPI Setup

### Clone the repository:

```sh
$ git clone git@github.com:ernest-rakhmatulin/coinapi.git
$ cd coinapi
```

### Run containers:

```sh
$ docker-compose up
```

### Apply database migrations

Connect to `application` container:

```sh
$ docker-compose exec application bash
```

Being connected to `application` container run migrations:

```sh
$ python manage.py migrate
```

### Create a superuser 

Being connected to `application` container run the 
command and follow the instructions.  

```sh
$ python manage.py createsuperuser
```

## Celery Beat setup

Celery beat is a scheduler. It kicks off tasks at regular intervals, 
that are then executed by available Celery worker nodes.

To schedule a task that will refresh currency rate once per hour 
connect to `application` container and run:

```sh
$ python manage.py init_celery_beat
```

This will schedule `core.tasks.refresh_currency_exchange_rate_task` 
to be executed every hour.

If you need to add new periodic tasks, or you need to update 
the schedule, you can do it manually through Django admin 
(/admin/django_celery_beat/).



