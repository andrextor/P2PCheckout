import unittest

from checkout.entities.token import Token


class TokenTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test the initialization of a Token object.
        """
        token = Token(
            token="12345",
            subtoken="67890",
            franchise="Visa",
            franchise_name="Visa International",
            issuer_name="Bank of Test",
            last_digits="1234",
            valid_until="2025-12-31",
            cvv="123",
            installments=12,
        )

        self.assertEqual(token.token, "12345")
        self.assertEqual(token.subtoken, "67890")
        self.assertEqual(token.franchise, "Visa")
        self.assertEqual(token.franchise_name, "Visa International")
        self.assertEqual(token.issuer_name, "Bank of Test")
        self.assertEqual(token.last_digits, "1234")
        self.assertEqual(token.valid_until, "2025-12-31")
        self.assertEqual(token.cvv, "123")
        self.assertEqual(token.installments, 12)

    def test_expiration_valid_date(self):
        """
        Test the expiration method with a valid date.
        """
        token = Token(valid_until="2025-12-31")
        self.assertEqual(token.expiration(), "12/25")

    def test_expiration_invalid_date(self):
        """
        Test the expiration method with an invalid date.
        """
        token = Token(valid_until="invalid-date")
        self.assertEqual(token.expiration(), "Invalid date")

    def test_expiration_empty_date(self):
        """
        Test the expiration method with an empty date.
        """
        token = Token(valid_until="")
        self.assertEqual(token.expiration(), "Invalid date")

    def test_to_dict(self):
        """
        Test the to_dict method.
        """
        token = Token(
            token="12345",
            subtoken="67890",
            franchise="Visa",
            franchise_name="Visa International",
            issuer_name="Bank of Test",
            last_digits="1234",
            valid_until="2025-12-31",
            cvv="123",
            installments=12,
        )

        expected_dict = {
            "token": "12345",
            "subtoken": "67890",
            "franchise": "Visa",
            "franchiseName": "Visa International",
            "issuerName": "Bank of Test",
            "lastDigits": "1234",
            "validUntil": "2025-12-31",
            "cvv": "123",
            "installments": 12,
        }

        self.assertEqual(token.to_dict(), expected_dict)
