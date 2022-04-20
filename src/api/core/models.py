from django.db import models
from .choices import CurrencyCodeChoices

class CurrencyExchangeRate(models.Model):
    from_code = models.CharField(max_length=3, choices=CurrencyCodeChoices.choices)
    to_code = models.CharField(max_length=3, choices=CurrencyCodeChoices.choices)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=8)
    bid_price = models.DecimalField(max_digits=15, decimal_places=8)
    ask_price = models.DecimalField(max_digits=15, decimal_places=8)
    refresh_time = models.DateTimeField(auto_now_add=True)
