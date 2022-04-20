import requests
from django.conf import settings

from core.models import CurrencyExchangeRate


def query_alphavantage(function: str, params: dict):
    url = 'https://www.alphavantage.co/query'
    query_params = {
        'function': function,
        'apikey': settings.ALPHA_VANTAGE_API_KEY,
        **params
    }
    response = requests.get(url, params=query_params)
    return response.json()


def refresh_currency_exchange_rate(from_currency, to_currency):
    function = 'CURRENCY_EXCHANGE_RATE'
    params = {'from_currency': from_currency, 'to_currency': to_currency}

    query_response = query_alphavantage(function=function, params=params)
    rate = query_response['Realtime Currency Exchange Rate']

    exchange_rate = CurrencyExchangeRate(
        from_code=rate.get("1. From_Currency Code"),
        to_code=rate.get("3. To_Currency Code"),
        exchange_rate=rate.get("5. Exchange Rate"),
        bid_price=rate.get("8. Bid Price"),
        ask_price=rate.get("9. Ask Price")
    )
    exchange_rate.save()

    return exchange_rate

