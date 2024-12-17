import unittest

from checkout.entities.name_value_pair import NameValuePair
from checkout.messages.requests.redirect import RedirectRequest


class RedirectRequestTest(unittest.TestCase):
    def test_initialization_with_minimal_data(self):
        """
        Test initialization of RedirectRequest with required fields only.
        """
        data = {"returnUrl": "https://example.com/return", "ipAddress": "192.168.1.1", "userAgent": "Test User Agent"}
        redirect_request = RedirectRequest(**data)

        self.assertEqual(redirect_request.return_url, "https://example.com/return")
        self.assertEqual(redirect_request.ip_address, "192.168.1.1")
        self.assertEqual(redirect_request.user_agent, "Test User Agent")
        self.assertEqual(redirect_request.locale, "es_CO")

    def test_initialization_with_all_fields(self):
        """
        Test initialization of RedirectRequest with all fields.
        """
        data = {
            "locale": "en_US",
            "payer": {"document": "123456789", "name": "John", "surname": "Doe"},
            "buyer": {"document": "987654321", "name": "Jane", "surname": "Doe"},
            "payment": {"reference": "TEST_REF", "amount": {"currency": "COP", "total": 10000}},
            "subscription": {"reference": "SUB123", "description": "Test Subscription"},
            "returnUrl": "https://example.com/return",
            "paymentMethod": "credit_card",
            "cancelUrl": "https://example.com/cancel",
            "ipAddress": "192.168.1.1",
            "userAgent": "Test User Agent",
            "expiration": "2023-12-31T23:59:59Z",
            "captureAddress": "true",
            "skipResult": True,
            "noBuyerFill": True,
        }
        redirect_request = RedirectRequest(**data)

        self.assertEqual(redirect_request.locale, "en_US")
        self.assertEqual(redirect_request.return_url, "https://example.com/return")
        self.assertEqual(redirect_request.payment_method, "credit_card")
        self.assertEqual(redirect_request.cancel_url, "https://example.com/cancel")
        self.assertEqual(redirect_request.ip_address, "192.168.1.1")
        self.assertEqual(redirect_request.user_agent, "Test User Agent")
        self.assertEqual(redirect_request.expiration, "2023-12-31T23:59:59Z")
        self.assertTrue(redirect_request.capture_address)
        self.assertTrue(redirect_request.skip_result)
        self.assertTrue(redirect_request.no_buyer_fill)

    def test_from_dict(self):
        """
        Test creating RedirectRequest from a dictionary.
        """
        data = {"returnUrl": "https://example.com/return", "ipAddress": "192.168.1.1", "userAgent": "Test User Agent"}
        redirect_request = RedirectRequest.model_validate(data)

        self.assertIsInstance(redirect_request, RedirectRequest)
        self.assertEqual(redirect_request.return_url, "https://example.com/return")
        self.assertEqual(redirect_request.ip_address, "192.168.1.1")
        self.assertEqual(redirect_request.user_agent, "Test User Agent")

    def test_to_dict(self):
        """
        Test converting RedirectRequest to a dictionary.
        """
        data = {
            "returnUrl": "https://example.com/return",
            "ipAddress": "192.168.1.1",
            "userAgent": "Test User Agent",
            "captureAddress": True,
            "cancel_url": "https://cancel.com/return",
            "payment": {
                "reference": "REF_123",
                "description": "DES_123",
                "amount": {"total": 1000, "currency": "COP"},
                "custom_fields": [NameValuePair(keyword="payment_field", value="payment")],
            },
            "custom_fields": [
                NameValuePair(keyword="field1", value="value1"),
                NameValuePair(keyword="field2", value="value2"),
            ],
        }
        redirect_request = RedirectRequest(**data)
        result = redirect_request.to_dict()

        expected = {
            "locale": "es_CO",
            "payment": {
                "reference": "REF_123",
                "description": "DES_123",
                "amount": {"currency": "COP", "total": 1000.0},
                "allowPartial": "false",
                "subscribe": "false",
                "fields": [{"keyword": "payment_field", "value": "payment", "displayOn": "none"}],
            },
            "returnUrl": "https://example.com/return",
            "cancelUrl": "https://cancel.com/return",
            "ipAddress": "192.168.1.1",
            "userAgent": "Test User Agent",
            "captureAddress": "true",
            "skipResult": "false",
            "noBuyerFill": "false",
            "fields": [
                {"keyword": "field1", "value": "value1", "displayOn": "none"},
                {"keyword": "field2", "value": "value2", "displayOn": "none"},
            ],
        }

        self.assertEqual(result, expected)

    def test_optional_fields_defaults(self):
        """
        Test that optional fields have correct default values.
        """
        data = {"returnUrl": "https://example.com/return", "ipAddress": "192.168.1.1", "userAgent": "Test User Agent"}
        redirect_request = RedirectRequest(**data)

        self.assertIsNone(redirect_request.payer)
        self.assertIsNone(redirect_request.buyer)
        self.assertIsNone(redirect_request.payment)
        self.assertIsNone(redirect_request.subscription)
        self.assertIsNone(redirect_request.expiration)
        self.assertIsNone(redirect_request.payment_method)
        self.assertIsNone(redirect_request.cancel_url)
