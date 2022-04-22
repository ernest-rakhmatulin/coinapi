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

#### First run 

We have two docker-compose files:
- `docker-compose.yml`
- `docker-compose-first-time.yml`

You may need `docker-compose-first-time.yml` only for the first run. It will 
trigger build, static collection, migrations. It will also initiate scheduler.  

```sh
$ docker-compose -f docker-compose.yml -f docker-compose-first-time.yml up
```

Done! Everything is up and running! [http://localhost/](http://localhost/)

#### Regular run 

Regular runs doesn't require `docker-compose-first-time.yml`. To run the application: 

```sh
$ docker-compose up
```

### Database migrations

To apply migratiosn connect to `application` container:

```sh
$ docker-compose exec application bash
```

Being connected to `application` container run migrations:

```sh
$ python manage.py migrate
```

### Superuser 

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

This will schedule `core.tasks.get_refreshed_currency_exchange_rates_task` 
to be executed every hour.

If you need to add new periodic tasks, or you need to update 
the schedule, you can do it manually through Django admin 
(/admin/django_celery_beat/).



