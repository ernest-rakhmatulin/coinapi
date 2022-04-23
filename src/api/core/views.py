from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import CurrencyCodeChoices
from core.serializers import CurrencyExchangeRateSerializerV1
from core.services import get_currency_exchange_rate, get_refreshed_currency_exchange_rate


class CurrencyExchangeRateView(APIView):
    currency_pair = dict(
        from_currency=CurrencyCodeChoices.BTC,
        to_currency=CurrencyCodeChoices.USD
    )

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return CurrencyExchangeRateSerializerV1

    def get(self, request):
        serializer_class = self.get_serializer_class()
        exchange_rate = get_currency_exchange_rate(**self.currency_pair)
        serializer = serializer_class(instance=exchange_rate)
        return Response(serializer.data)

    def post(self, request):
        serializer_class = self.get_serializer_class()
        exchange_rate = get_refreshed_currency_exchange_rate(**self.currency_pair)
        serializer = serializer_class(instance=exchange_rate)
        return Response(serializer.data)
