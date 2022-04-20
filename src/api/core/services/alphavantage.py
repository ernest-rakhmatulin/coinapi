import requests
from django.conf import settings

DEFAULT_FUNCTION = 'CURRENCY_EXCHANGE_RATE'
DEFAULT_PARAMS = {'from_currency': 'BTC', 'to_currency': 'USD'}


def query_alphavantage(function: str, params: dict):
    query_params = {
        'function': function,
        'apikey': settings.ALPHA_VANTAGE_API_KEY,
        **params
    }

    url = 'https://www.alphavantage.co/query'
    response = requests.get(url, params=query_params)
    return response.json()


x = query_alphavantage(function=DEFAULT_FUNCTION, params=DEFAULT_PARAMS)
print(x)
