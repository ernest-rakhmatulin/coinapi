import base64
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import CurrencyExchangeRate
from core.tasks import get_refreshed_currency_exchange_rates_task


class CurrencyExchangeRateViewTest(APITestCase):

    def setUp(self):
        username = 'johndoe'
        email = 'johndoe@example.com'
        password = 'johnpassword'
        self.user = User.objects.create_user(username, email, password)
        token = base64.b64encode(f'{username}:{password}'.encode()).decode()
        self.auth_header = f"Basic {token}"

    def test_unauthorized(self):
        response = self.client.get(reverse('currency-exchange-rate'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_request(self):
        # This test covers 3 types of AlphaVantage responses.
        # OK, Note, Error.

        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)

        with patch("core.services.query_alphavantage") as currency_rate:
            alphavantage_ok_response = {
                "Realtime Currency Exchange Rate": {
                    "1. From_Currency Code": "BTC",
                    "2. From_Currency Name": "Bitcoin",
                    "3. To_Currency Code": "USD",
                    "4. To_Currency Name": "United States Dollar",
                    "5. Exchange Rate": "39445.08000000",
                    "6. Last Refreshed": "2022-04-22 20:27:01",
                    "7. Time Zone": "UTC",
                    "8. Bid Price": "39445.08000000",
                    "9. Ask Price": "39445.09000000"
                }
            }

            # we don't need actual error and note messages, we just
            # check cases when the response has this attributes.

            alphavantage_error_response = {
                "Error Message": True
            }
            alphavantage_note_response = {
                "Note": True
            }

            currency_rate.side_effect = [
                alphavantage_ok_response,
                alphavantage_error_response,
                alphavantage_note_response
            ]

            success_response = self.client.post(reverse('currency-exchange-rate'))
            self.assertEqual(
                success_response.json().get('exchange_rate'),
                alphavantage_ok_response['Realtime Currency Exchange Rate']['5. Exchange Rate']
            )
            self.assertEqual(
                success_response.status_code,
                status.HTTP_200_OK
            )

            error_response = self.client.post(reverse('currency-exchange-rate'))
            self.assertEqual(
                'Data provider API error. Please contact customer support.',
                error_response.json()['detail']
            )
            self.assertEqual(
                error_response.status_code,
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            note_response = self.client.post(reverse('currency-exchange-rate'))
            self.assertEqual(
                'The limit of requests per minute to the data provider has been reached. '
                'Wait for a minute, or try GET request, to get latest available rate.',
                note_response.json()['detail']
            )
            self.assertEqual(
                note_response.status_code,
                status.HTTP_429_TOO_MANY_REQUESTS
            )

    def test_get_request(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(reverse('currency-exchange-rate'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TasksTestCase(TestCase):

    def test_get_refreshed_currency_exchange_rates_task_create(self):
        with patch("core.services.query_alphavantage") as currency_rate:
            currency_rate.return_value = {
                "Realtime Currency Exchange Rate": {
                    "1. From_Currency Code": "BTC",
                    "2. From_Currency Name": "Bitcoin",
                    "3. To_Currency Code": "USD",
                    "4. To_Currency Name": "United States Dollar",
                    "5. Exchange Rate": "39445.08000000",
                    "6. Last Refreshed": "2022-04-22 20:27:01",
                    "7. Time Zone": "UTC",
                    "8. Bid Price": "39445.08000000",
                    "9. Ask Price": "39445.09000000"
                }
            }
            get_refreshed_currency_exchange_rates_task()
            self.assertEqual(
                CurrencyExchangeRate.objects.count(), 1,
                'New object must be created.'
            )

    def test_get_refreshed_currency_exchange_rates_task_skip(self):
        # Creating an object, that is fresh enough to skip refreshing
        CurrencyExchangeRate.objects.create(
            from_code="BTC",
            to_code="USD",
            exchange_rate=39445.08000000,
            bid_price=39445.08000000,
            ask_price=39445.09000000,
        )

        with patch("core.services.query_alphavantage") as currency_rate:
            currency_rate.return_value = {
                "Realtime Currency Exchange Rate": {
                    "1. From_Currency Code": "BTC",
                    "2. From_Currency Name": "Bitcoin",
                    "3. To_Currency Code": "USD",
                    "4. To_Currency Name": "United States Dollar",
                    "5. Exchange Rate": "39445.08000000",
                    "6. Last Refreshed": "2022-04-22 20:27:01",
                    "7. Time Zone": "UTC",
                    "8. Bid Price": "39445.08000000",
                    "9. Ask Price": "39445.09000000"
                }
            }
            self.assertEqual(
                CurrencyExchangeRate.objects.count(), 1,
                'Fresh object should already exist.'
            )

            get_refreshed_currency_exchange_rates_task()

            self.assertEqual(
                CurrencyExchangeRate.objects.count(), 1,
                'Object should not be created, as we already have a fresh object.'
            )
