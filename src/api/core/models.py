from django.db import models

from .choices import CurrencyCodeChoices


class CurrencyExchangeRate(models.Model):
    from_code = models.CharField(max_length=3, choices=CurrencyCodeChoices.choices)
    to_code = models.CharField(max_length=3, choices=CurrencyCodeChoices.choices)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=8)
    bid_price = models.DecimalField(max_digits=15, decimal_places=8)
    ask_price = models.DecimalField(max_digits=15, decimal_places=8)
    refresh_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This index makes sense if we have several currency pairs.
        # If it is assumed that there will always be only one pair,
        # it can be removed, since there is a primary key
        indexes = [
            models.Index(fields=['from_code', 'to_code']),
        ]

    def __str__(self):
        return f'{self.from_code}/{self.to_code}, exchange_rate: ' \
               f'{self.exchange_rate}, refresh_time: {self.refresh_time}'
