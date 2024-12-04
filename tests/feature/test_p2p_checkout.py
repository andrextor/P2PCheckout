import unittest
from unittest.mock import patch

from cases.redirect_response_mock import RedirectResponseMock
from entities.instrument import Instrument
from entities.token import Token
from enums.status_enum import StatusEnum
from exceptions.p2p_exception import P2PException
from messages.requests.collect import CollectRequest
from messages.requests.redirect import RedirectRequest
from messages.responses.information import InformationResponse
from messages.responses.redirect import RedirectResponse
from messages.responses.reverse import ReverseResponse
from p2p_checkout import P2PCheckout


class P2PCheckoutTest(unittest.TestCase):

    def setUp(self):
        """Set up shared test data."""
        self.settings_data = {
            "base_url": "https://example.com",
            "login": "test_login",
            "tranKey": "test_tranKey",
            "timeout": 10,
        }
        self.p2p_checkout = P2PCheckout(self.settings_data)

    def test_initialization(self):
        """Test if the P2PCheckout initializes correctly."""
        self.assertIsNotNone(self.p2p_checkout.settings)
        self.assertEqual(str(self.p2p_checkout.settings.base_url), "https://example.com/")

    def test_validate_request_invalid(self):
        """Test _validate_request with an invalid type."""
        with self.assertRaises(P2PException) as context:
            self.p2p_checkout._validate_request([], RedirectRequest)

        self.assertIn("Invalid request type: list. Expected RedirectRequest.", str(context.exception))

    def test_validate_request_invalid_dict_conversion(self):
        """
        Test _validate_request with a dictionary that cannot be converted to the expected class.
        """
        invalid_dict = {"invalid_field": "value"}
        with self.assertRaises(P2PException) as context:
            self.p2p_checkout._validate_request(invalid_dict, RedirectRequest)

        self.assertIn("Failed to convert dictionary to RedirectRequest", str(context.exception))

    @patch("clients.rest_client.RestCarrier._post")
    @RedirectResponseMock.mock_response_decorator("redirect_response_successful", 200)
    def test_validate_request_valid(self, mock_post, mock_response):
        """Test _validate_request with a valid RedirectRequest and mock RestCarrier."""
        mock_post.return_value = mock_response["body"]
        redirect_request = {
            "returnUrl": "https://example.com/return",
            "ipAddress": "127.0.0.1",
            "userAgent": "P2PCheckout Sandbox",
        }

        request = self.p2p_checkout._validate_request(redirect_request, RedirectRequest)
        redirect_request = self.p2p_checkout.request(redirect_request=request)

        self.assertIsInstance(redirect_request, RedirectResponse)
        self.assertEqual(redirect_request.request_id, 1)
        self.assertEqual(
            redirect_request.process_url,
            "https://checkout-co.placetopay.dev/spa/session/1/8618851565b57b1c44d7576c4bba9b91",
        )
        self.assertEqual(redirect_request.status.status, StatusEnum.OK)
        self.assertEqual(redirect_request.status.reason, "PC")
        self.assertEqual(redirect_request.status.message, "The request has been processed correctly")
        self.assertIsNotNone(redirect_request.status.date)

    @patch("clients.rest_client.RestCarrier._post")
    @RedirectResponseMock.mock_response_decorator("information_subscription_response_successful", 200)
    def test_query_subscription_valid(self, mock_post, mock_response):
        """
        Test the query method with a valid request ID and mock response.
        """
        mock_post.return_value = mock_response["body"]

        information_response = self.p2p_checkout.query("88860")

        self.assertIsInstance(information_response, InformationResponse)
        self.assertEqual(information_response.request_id, 88860)
        self.assertEqual(information_response.status.status, "APPROVED")
        self.assertEqual(information_response.status.reason, "00")
        self.assertEqual(information_response.status.message, "The request has been successfully approved")
        self.assertIsNotNone(information_response.status.date)

        self.assertIsNotNone(information_response.request)
        self.assertEqual(information_response.request.locale, "en_US")
        self.assertEqual(information_response.request.payer.document, "118877455")
        self.assertEqual(information_response.request.payer.name, "John")
        self.assertEqual(information_response.request.return_url, "https://www.google.com")

        self.assertIsNotNone(information_response.subscription)
        self.assertEqual(information_response.subscription.type, "token")
        self.assertEqual(information_response.subscription.status.status, "OK")
        self.assertEqual(information_response.subscription.status.reason, "00")
        self.assertEqual(
            information_response.subscription.status.message, "The request has been successfully processed"
        )

        self.assertIsNotNone(information_response.subscription.instrument)
        self.assertEqual(len(information_response.subscription.instrument), 8)
        self.assertEqual(information_response.subscription.instrument[0].keyword, "token")
        self.assertEqual(
            information_response.subscription.instrument[0].value,
            "71f293122c1ed577974f2249c9449c648d8dcb104cb531f2c77e3b6c8910aca0",
        )
        self.assertEqual(information_response.subscription.instrument[1].keyword, "subtoken")
        self.assertEqual(information_response.subscription.instrument[1].value, "2964322564071111")

        self.assertIsNone(information_response.payment)

        self.assertIsNone(information_response.last_transaction())
        self.assertIsNone(information_response.last_approved_transaction())
        self.assertEqual(information_response.last_authorization(), "")

    @patch("clients.rest_client.RestCarrier._post")
    @RedirectResponseMock.mock_response_decorator("information_payment_response_successful", 200)
    def test_query_payment_valid(self, mock_post, mock_response):
        """
        Test the query method with a valid request ID and mock response.
        """
        mock_post.return_value = mock_response["body"]

        information_response = self.p2p_checkout.query("88867")

        self.assertIsInstance(information_response, InformationResponse)
        self.assertEqual(information_response.request_id, 88867)
        self.assertEqual(information_response.status.status, "APPROVED")
        self.assertEqual(information_response.status.reason, "00")
        self.assertEqual(information_response.status.message, "The request has been successfully approved")
        self.assertIsNotNone(information_response.status.date)

        self.assertEqual(len(information_response.payment), 2)

        payment_1 = information_response.payment[0]
        self.assertEqual(payment_1.reference, "test_megapuntos_test_3")
        self.assertEqual(payment_1.authorization, "999999")
        self.assertEqual(payment_1.payment_method, "diners")
        self.assertEqual(payment_1.status.status, "APPROVED")
        self.assertEqual(payment_1.status.reason, "00")
        self.assertEqual(payment_1.amount.fromAmount.total, 10000)
        self.assertEqual(payment_1.amount.fromAmount.currency, "COP")
        self.assertEqual(payment_1.amount.toAmount.total, 2.24)
        self.assertEqual(payment_1.amount.toAmount.currency, "USD")

        payment_2 = information_response.payment[1]
        print(payment_2)
        self.assertEqual(payment_2.reference, "test_megapuntos_test_3")
        self.assertEqual(payment_2.authorization, "000000")
        self.assertEqual(payment_2.payment_method, "master")
        self.assertEqual(payment_2.status.status, "REJECTED")
        self.assertEqual(payment_2.status.reason, "?2")

        self.assertEqual(payment_2.amount.fromAmount.total, 10000)
        self.assertEqual(payment_2.amount.fromAmount.currency, "COP")
        self.assertEqual(payment_2.amount.toAmount.total, 2178.45)
        self.assertEqual(payment_2.amount.toAmount.currency, "CLP")

    @patch("clients.rest_client.RestCarrier._post")
    @RedirectResponseMock.mock_response_decorator("collect_response_successful", 200)
    def test_collect_valid(self, mock_post, mock_response):
        """
        Test the collect method with a valid CollectRequest and mock response.
        """
        mock_post.return_value = mock_response["body"]

        token = Token(token="test_token", subtoken="test_subtoken")
        instrument = Instrument(token=token, pin="1234", password="secret")
        collect_request_data = {
            "instrument": instrument,
            "returnUrl": "https://checkout-co.placetopay.dev/home",
            "ipAddress": "186.86.52.226",
            "userAgent": "PostmanRuntime/7.42.0",
        }
        collect_request = CollectRequest.model_validate(collect_request_data)

        result = self.p2p_checkout.collect(collect_request)

        self.assertIsInstance(result, InformationResponse)
        self.assertEqual(result.request_id, 88866)
        self.assertEqual(result.status.status, "APPROVED")
        self.assertEqual(result.status.reason, "00")
        self.assertEqual(result.status.message, "La petición ha sido aprobada exitosamente")
        self.assertIsNotNone(result.status.date)

        self.assertEqual(len(result.payment), 1)

        payment = result.payment[0]
        self.assertEqual(payment.reference, "ref_collect_3")
        self.assertEqual(payment.authorization, "300159")
        self.assertEqual(payment.payment_method, "master")
        self.assertEqual(payment.status.status, "APPROVED")
        self.assertEqual(payment.status.message, "Aprobada")
        self.assertEqual(payment.amount.fromAmount.total, 10000)
        self.assertEqual(payment.amount.fromAmount.currency, "COP")
        self.assertEqual(payment.amount.toAmount.total, 2178.45)
        self.assertEqual(payment.amount.toAmount.currency, "CLP")

    @patch("clients.rest_client.RestCarrier._post")
    @RedirectResponseMock.mock_response_decorator("reverse_response_successful", 200)
    def test_reverse_valid(self, mock_post, mock_response):
        """
        Test the reverse method with a valid internal reference and mock response.
        """
        mock_post.return_value = mock_response["body"]

        internal_reference = "437987"
        result = self.p2p_checkout.reverse(internal_reference)

        self.assertIsInstance(result, ReverseResponse)
        self.assertIsNotNone(result.status)
        self.assertEqual(result.status.status, "APPROVED")
        self.assertEqual(result.status.reason, "00")
        self.assertEqual(result.status.message, "Aprobada")
        self.assertIsNotNone(result.status.date)

        self.assertIsNotNone(result.payment)
        payment = result.payment
        self.assertEqual(payment.reference, "ref_collect_3")
        self.assertEqual(payment.authorization, "300159")
        self.assertEqual(payment.payment_method, "master")
        self.assertEqual(payment.status.status, "APPROVED")
        self.assertEqual(payment.amount.fromAmount.total, 10000)
        self.assertEqual(payment.amount.fromAmount.currency, "COP")
        self.assertEqual(payment.amount.toAmount.total, 2178.45)
        self.assertEqual(payment.amount.toAmount.currency, "CLP")

        self.assertEqual(len(payment.processor_fields), 9)
        self.assertEqual(payment.processor_fields[0].keyword, "merchantCode")
        self.assertEqual(payment.processor_fields[0].value, "4549106521651")
        self.assertEqual(payment.processor_fields[1].keyword, "terminalNumber")
        self.assertEqual(payment.processor_fields[1].value, "98765432")
        self.assertEqual(payment.processor_fields[-1].keyword, "b24")
        self.assertEqual(payment.processor_fields[-1].value, "00")