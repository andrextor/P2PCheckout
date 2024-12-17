import unittest

from checkout.entities.instrument import Instrument
from checkout.entities.token import Token
from checkout.messages.requests.collect import CollectRequest


class CollectTest(unittest.TestCase):

    def setUp(self):
        self.token_data = {
            "token": "test_token",
            "subtoken": "test_subtoken",
            "franchise": "visa",
            "franchiseName": "Visa",
            "issuerName": "Test Issuer",
            "lastDigits": "1234",
            "validUntil": "2025-12-31",
            "cvv": "123",
            "installments": 12,
        }

        self.token = Token(**self.token_data)
        self.instrument = Instrument(token=self.token, pin="1234", password="secret")
        self.request_data = {
            "instrument": self.instrument,
            "returnUrl": "https://example.com/return",
            "ipAddress": "192.168.1.1",
            "userAgent": "Mozilla/5.0",
        }

    def test_initialization_with_token(self):
        """
        Test CollectRequest initialization with a Token in the Instrument.
        """
        collect_request = CollectRequest(**self.request_data)

        self.assertIsNotNone(collect_request.instrument)
        self.assertIsInstance(collect_request.instrument, Instrument)
        self.assertIsInstance(collect_request.instrument.token, Token)
        self.assertEqual(collect_request.instrument.token.token, self.token_data["token"])
        self.assertEqual(collect_request.instrument.token.franchise, self.token_data["franchise"])
        self.assertEqual(collect_request.instrument.pin, "1234")
        self.assertEqual(collect_request.instrument.password, "secret")
        self.assertEqual(collect_request.return_url, self.request_data["returnUrl"])
        self.assertEqual(collect_request.ip_address, self.request_data["ipAddress"])
        self.assertEqual(collect_request.user_agent, self.request_data["userAgent"])

    def test_to_dict_with_token(self):
        """
        Test CollectRequest to_dict method with a Token in the Instrument.
        """
        collect_request = CollectRequest(**self.request_data)
        result = collect_request.to_dict()

        self.assertIn("instrument", result)
        self.assertEqual(result["instrument"]["token"]["token"], self.token_data["token"])
        self.assertEqual(result["instrument"]["token"]["franchise"], self.token_data["franchise"])
        self.assertEqual(result["instrument"]["pin"], "1234")
        self.assertEqual(result["instrument"]["password"], "secret")

    def test_to_dict_without_token(self):
        """
        Test CollectRequest to_dict method with no Token in the Instrument.
        """
        request_data_no_token = self.request_data.copy()
        request_data_no_token["instrument"] = Instrument(pin="5678", password="no_token")

        collect_request = CollectRequest(**request_data_no_token)
        result = collect_request.to_dict()

        self.assertIn("instrument", result)
        self.assertEqual(result["instrument"]["pin"], "5678")
        self.assertEqual(result["instrument"]["password"], "no_token")
        self.assertEqual("es_CO", result["locale"])
        self.assertEqual("192.168.1.1", result["ipAddress"])
        self.assertEqual("Mozilla/5.0", result["userAgent"])
        self.assertEqual("https://example.com/return", result["returnUrl"])

        self.assertEqual("false", result["captureAddress"])
        self.assertEqual("false", result["skipResult"])
        self.assertEqual("false", result["noBuyerFill"])
