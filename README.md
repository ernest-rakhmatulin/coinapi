# CoinAPI

### Clone the repository:

```sh
git clone git@github.com:ernest-rakhmatulin/coinapi.git
cd coinapi
```

### Run containers:

#### First run 

We have two docker-compose files:
- `docker-compose.yml`
- `docker-compose-first-time.yml`

You may need `docker-compose-first-time.yml` only for the first run. It will 
trigger build, static collection, migrations. It will also initiate scheduler.  

```sh
docker-compose -f docker-compose.yml -f docker-compose-first-time.yml up
```

Done! Everything is up and running! [http://localhost/](http://localhost/)

In case of errors try:  

```sh
docker-compose down --remove-orphans --volumes
docker-compose -f docker-compose.yml -f docker-compose-first-time.yml up
```


#### Regular run 

Regular runs doesn't require `docker-compose-first-time.yml`. To run the application: 

```sh
docker-compose up -f docker-compose.yml
```

or: 

```sh
docker-compose up
```

_________________________________________________________________________________


# Backend Task

### Write an API using Django that fetches the price of BTC/USD from the alphavantage API every hour, and stores it on postgres. 
_________________________________________________________________________________

To implement this feature I used **Celery** + **Celery Beat**.

`core.tasks.get_refreshed_currency_exchange_rates_task`

The task iterates through all currency pairs listed in `settings.CURRENCY_PAIRS`
only (BTC-USD now) and refreshes values. If task fails because of an exception 
it is restarted 5 times `max_retries=5`. 

Restarted task checks currency pair's `refresh_time`, and skip refreshed currency pairs.    
_________________________________________________________________________________

Scheduling can be done via Django admin, or via `manage.py init_celery_beat`.

```sh
python manage.py init_celery_beat
```

This will create an hour interval for Celery Beat, and schedule 
`core.tasks.get_refreshed_currency_exchange_rates_task` to be executed once per interval.

###This API must be secured which means that you will need an API key to use it. 

To make all urls secured I added `DEFAULT_PERMISSION_CLASSES` and 
`DEFAULT_AUTHENTICATION_CLASSES`.

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    ),
    ...
}
```

### Endpoint's versioning 

There should be two endpoints: 

GET /api/v1/quotes - returns exchange rate 
POST /api/v1/quotes - triggers force requesting the prices from alphavantage. 


According to urls it was required to add the support of versioning. 
I've used `rest_framework.versioning.NamespaceVersioning`, because it allows 
supporting of requested urls' style: `/api/v1/<resource>`.

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ('v1',),
    'VERSION_PARAM': 'version'
}
```
_________________________________________________________________________________

The view `core.views.CurrencyExchangeRateView` supports versioning. It selects a serializer
based on request url.

```python
def get_serializer_class(self):
    if self.request.version == 'v1':
        return CurrencyExchangeRateSerializerV1
```
_________________________________________________________________________________

Versioning is also supported by tests. 

```python
error_response = self.client.post(reverse('v1:currency-exchange-rate'))
```

### The API & DB should be containerized using Docker as well. The technologies to be used: Celery, Redis or RabbitMQ, Docker and Docker Compose. 

All dependencies are containerized. We have `nginx`, `postgres`, `redis`, `application`,
`celery_worker`, `celery_beat` containers. Last 3 uses same image.

#### Every part should be implemented as simple as possible.
To make it as simple as possible I moved all possible settings to `settings.REST_FRAMEWORK`.
All containers use default images from hub, or single custom build image.

#### The project should be committed to GitHub. 
https://github.com/ernest-rakhmatulin/coinapi

#### The sensitive data such as alphavantage API key, should be passed from the .env
All variables moved to `variables.env`. These variables are shared between all containers.

```sh
POSTGRES_USER=coin-project-user
POSTGRES_PASSWORD=QHwM~7dfusDDk
POSTGRES_DB=coin-project-db
POSTGRES_HOST=postgres

CELERY_BROKER_URL=redis://redis:6379
CELERY_RESULT_BACKEND=redis://redis:6379

SECRET_KEY=jWnZr4u7x!z%C*F-JaNdRgUkXp2s5v8y/B?DJaNdRgUkXp2s5v8y/B?D
ALPHA_VANTAGE_API_KEY=VPO8KG64PZW9TZ33

STATIC_URL=/static/
```

Variables are used via `os.environ` like this:

```python
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': '',
    }
}
...
```

