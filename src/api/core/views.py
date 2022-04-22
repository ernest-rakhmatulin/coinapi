from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import CurrencyCodeChoices
from core.serializers import CurrencyExchangeRateSerializer
from core.services import get_currency_exchange_rate, get_refreshed_currency_exchange_rate


class CurrencyExchangeRateView(APIView):
    currency_pair = dict(
        from_currency=CurrencyCodeChoices.BTC,
        to_currency=CurrencyCodeChoices.USD
    )

    def get(self, request):
        exchange_rate = get_currency_exchange_rate(**self.currency_pair)
        serializer = CurrencyExchangeRateSerializer(instance=exchange_rate)
        return Response(serializer.data)

    def post(self, request):
        exchange_rate = get_refreshed_currency_exchange_rate(**self.currency_pair)
        serializer = CurrencyExchangeRateSerializer(instance=exchange_rate)
        return Response(serializer.data)
