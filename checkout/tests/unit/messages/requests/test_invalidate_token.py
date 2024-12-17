import unittest

from checkout.entities.instrument import Instrument
from checkout.messages.requests.invalidate_token import InvalidateToKenRequest


class InvalidateTokenRequestTest(unittest.TestCase):
    def test_to_dic_valid(self):
        """Test to_dic returns the correct dictionary format."""
        instrument = Instrument(**{"token": {"token": "test_token", "subtoken": "test_subtoken"}})
        request = InvalidateToKenRequest(locale="en_US", instrument=instrument)

        expected_output = {
            "locale": "en_US",
            "instrument": {"token": {"token": "test_token", "subtoken": "test_subtoken"}},
        }

        self.assertEqual(request.to_dic(), expected_output)

    def test_to_dic_default_locale(self):
        """Test to_dic with default locale value."""
        instrument = Instrument(**{"token": {"token": "test_token", "subtoken": "test_subtoken"}})
        request = InvalidateToKenRequest(instrument=instrument)

        expected_output = {
            "locale": "es_CO",
            "instrument": {"token": {"token": "test_token", "subtoken": "test_subtoken"}},
        }

        self.assertEqual(request.to_dic(), expected_output)
