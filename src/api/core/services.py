import requests
from django.conf import settings
from rest_framework.exceptions import APIException

from core.models import CurrencyExchangeRate


def query_alphavantage(function, params):
    """
    Gets function name, and query parameters, and returns a dict
    with data from AlphaVantage API

    Args:
        function (str): AlphaVantage API function name
        params (dict): query parameters

    Returns:
        dict: API response based dict
    """

    url = 'https://www.alphavantage.co/query'
    query_params = {
        'function': function,
        'apikey': settings.ALPHA_VANTAGE_API_KEY,
        **params
    }
    response = requests.get(url, params=query_params)
    result = response.json()

    # Alpha Vantage API returns a 'Note' when it reaches the limit.
    rate_limit_note = result.get('Note')
    if rate_limit_note:
        raise APIException('Alpha Vantage API rate limit. Wait for a minute, '
                           'or try GET request, to get latest available rate.')

    return response.json()


def get_currency_exchange_rate_alphavantage(from_currency, to_currency):
    """
    Gets a pair of currency codes, and fetches exchange rates data
    from AlphaVantage API for current pair. Prepares a dict of exchange
    rates data for CurrencyExchangeRate model, and returns it.

    Args:
        from_currency (str): Currency code "from"
        to_currency (str): Currency code "to"

    Returns:
        dict: a dict with data prepared for CurrencyExchangeRate model
    """

    query_response = query_alphavantage(
        function='CURRENCY_EXCHANGE_RATE',
        params={
            'from_currency': from_currency,
            'to_currency': to_currency
        }
    )
    rate = query_response['Realtime Currency Exchange Rate']
    return dict(
        from_code=rate.get("1. From_Currency Code"),
        to_code=rate.get("3. To_Currency Code"),
        exchange_rate=rate.get("5. Exchange Rate"),
        bid_price=rate.get("8. Bid Price"),
        ask_price=rate.get("9. Ask Price")
    )


def get_currency_exchange_rate(from_currency, to_currency):
    """
    Gets a pair of currency codes, and returns latest
    CurrencyExchangeRate object from the database.

    Args:
        from_currency (str): Currency code "from"
        to_currency (str): Currency code "to"

    Returns:
        CurrencyExchangeRate: last object with refreshed data
    """

    return CurrencyExchangeRate.objects.filter(
        from_code=from_currency,
        to_code=to_currency,
    ).last()


def get_refreshed_currency_exchange_rate(from_currency, to_currency):
    """
    Gets a pair of currency codes, gets data from AlphaVantage API,
    and creates a CurrencyExchangeRate record in database.
    Returns CurrencyExchangeRate object.

    Args:
        from_currency (str): Currency code "from"
        to_currency (str): Currency code "to"

    Returns:
        CurrencyExchangeRate: an object with refreshed data
    """
    exchange_rate_data = get_currency_exchange_rate_alphavantage(
        from_currency=from_currency,
        to_currency=to_currency
    )
    exchange_rate = CurrencyExchangeRate(**exchange_rate_data)
    exchange_rate.save()
    return exchange_rate
