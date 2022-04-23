from django.urls import path
from core.views import CurrencyExchangeRateView

app_name = 'core'

urlpatterns = [
    path('quotes', CurrencyExchangeRateView.as_view(), name='currency-exchange-rate')
]
