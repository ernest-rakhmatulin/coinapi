from rest_framework import serializers

from core.models import CurrencyExchangeRate


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = ['from_code', 'to_code', 'exchange_rate', 'bid_price', 'ask_price', 'refresh_time']
