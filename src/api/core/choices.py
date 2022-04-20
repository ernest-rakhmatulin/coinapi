from django.db.models import TextChoices

class CurrencyCodeChoices(TextChoices):
    USD = 'USD'
    BTC = 'BTC'