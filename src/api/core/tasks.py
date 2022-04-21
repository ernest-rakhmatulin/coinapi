from celery import shared_task
from core.services.alphavantage import get_refreshed_currency_exchange_rate
from django.conf import settings
from core.models import CurrencyExchangeRate
from django.utils import timezone


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 5, 'countdown': 10})
def get_refreshed_currency_exchange_rates_task(self):
    """
    Updates the exchange rates for all tracked
    currency pairs listed in settings.CURRENCY_PAIRS
    """

    for from_currency, to_currency in settings.CURRENCY_PAIRS:

        # Checks if pair record with refresh_time greater than certain time,
        # to make sure we don't fetch data that already has an actual record.
        rate_is_fresh = CurrencyExchangeRate.objects.filter(
            from_code=from_currency,
            to_code=to_currency,
            refresh_time__gt=timezone.now() - timezone.timedelta(hours=settings.REFRESH_RATE_HOURS)
        ).exists()

        # refreshing the rate if fresh rate doesn't exist
        if not rate_is_fresh:
            get_refreshed_currency_exchange_rate(
                from_currency=from_currency,
                to_currency=to_currency
            )


