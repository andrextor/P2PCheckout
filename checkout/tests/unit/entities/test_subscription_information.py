import unittest

from checkout.entities.account import Account
from checkout.entities.name_value_pair import NameValuePair
from checkout.entities.status import Status
from checkout.entities.subscription_information import SubscriptionInformation
from checkout.entities.token import Token
from checkout.enums.status_enum import StatusEnum


class SubsCriptionInformationTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test initialization with default values.
        """
        subscription = SubscriptionInformation()
        self.assertEqual(subscription.type, "")
        self.assertIsNone(subscription.status)
        self.assertEqual(subscription.instrument, [])

    def test_set_instrument_with_dict(self):
        """
        Test setting instrument with dictionary data.
        """
        instrument_data = {"item": [{"keyword": "key1", "value": "value1"}]}
        subscription = SubscriptionInformation()
        subscription.set_instrument(instrument_data)

        self.assertEqual(len(subscription.instrument), 1)
        self.assertEqual(subscription.instrument[0].keyword, "key1")
        self.assertEqual(subscription.instrument[0].value, "value1")

    def test_set_instrument_with_list(self):
        """
        Test setting instrument with a list of dictionaries.
        """
        instrument_data = [{"keyword": "key1", "value": "value1"}]
        subscription = SubscriptionInformation()
        subscription.set_instrument(instrument_data)

        self.assertEqual(len(subscription.instrument), 1)
        self.assertEqual(subscription.instrument[0].keyword, "key1")
        self.assertEqual(subscription.instrument[0].value, "value1")

    def test_instrument_to_list(self):
        """
        Test converting instrument to a list of dictionaries.
        """
        instrument_data = [
            NameValuePair(keyword="key1", value="value1"),
            NameValuePair(keyword="key2", value="value2"),
        ]
        subscription = SubscriptionInformation(instrument=instrument_data)
        instrument_list = subscription.instrument_to_list()

        self.assertEqual(len(instrument_list), 2)
        self.assertEqual(instrument_list[0]["keyword"], "key1")
        self.assertEqual(instrument_list[1]["value"], "value2")

    def test_parse_instrument_as_token(self):
        """
        Test parsing instrument as a Token.
        """

        instrument_data = [
            NameValuePair(keyword="token", value="12345"),
            NameValuePair(keyword="subtoken", value="54321"),
            NameValuePair(keyword="franchise", value="visa"),
            NameValuePair(keyword="franchiseName", value="Visa"),
            NameValuePair(keyword="validUntil", value="2025-12-31"),
        ]
        subscription = SubscriptionInformation(
            type="token", status=Status.quick(status=StatusEnum.OK, reason="00"), instrument=instrument_data
        )
        result = subscription.parse_instrument()

        self.assertIsInstance(result, Token)
        self.assertEqual(result.token, "12345")
        self.assertEqual(result.subtoken, "54321")
        self.assertEqual(result.franchise, "visa")
        self.assertEqual(result.valid_until, "2025-12-31")

    def test_parse_instrument_as_account(self):
        """
        Test parsing instrument as an Account.
        """

        instrument_data = [
            NameValuePair(keyword="bankCode", value="001"),
            NameValuePair(keyword="bankName", value="Bank A"),
            NameValuePair(keyword="accountType", value="savings"),
            NameValuePair(keyword="accountNumber", value="123456789"),
        ]
        subscription = SubscriptionInformation(
            type="account", status=Status.quick(status=StatusEnum.OK, reason="00"), instrument=instrument_data
        )
        result = subscription.parse_instrument()

        self.assertIsInstance(result, Account)
        self.assertEqual(result.bankCode, "001")
        self.assertEqual(result.bankName, "Bank A")
        self.assertEqual(result.accountType, "savings")
        self.assertEqual(result.accountNumber, "123456789")

    def test_set_instrument_list_of_dicts(self):
        """
        Test setting instrument when input is a list of dictionaries.
        """
        instrument_data = [{"keyword": "key1", "value": "value1"}]
        subscription = SubscriptionInformation()
        subscription.set_instrument(instrument_data)

        self.assertEqual(len(subscription.instrument), 1)
        self.assertIsInstance(subscription.instrument[0], NameValuePair)
        self.assertEqual(subscription.instrument[0].keyword, "key1")
        self.assertEqual(subscription.instrument[0].value, "value1")

    def test_set_instrument_list_of_name_value_pairs(self):
        """
        Test setting instrument when input is a list of NameValuePair objects.
        """
        nvp = NameValuePair(keyword="key1", value="value1")
        subscription = SubscriptionInformation()
        subscription.set_instrument([nvp])

        self.assertEqual(len(subscription.instrument), 1)
        self.assertIsInstance(subscription.instrument[0], NameValuePair)
        self.assertEqual(subscription.instrument[0].keyword, "key1")
        self.assertEqual(subscription.instrument[0].value, "value1")

    def test_parse_instrument_no_type(self):
        """
        Test parsing instrument with no type set.
        """
        instrument_data = [
            NameValuePair(keyword="key1", value="value1"),
        ]
        subscription = SubscriptionInformation(instrument=instrument_data)
        result = subscription.parse_instrument()

        self.assertIsNone(result)

    def test_to_dict(self):
        """
        Test conversion of SubscriptionInformation to dictionary.
        """

        instrument_data = [
            NameValuePair(keyword="key1", value="value1"),
        ]
        subscription = SubscriptionInformation(
            type="token", status=Status.quick(status=StatusEnum.OK, reason="00"), instrument=instrument_data
        )
        result_dict = subscription.to_dict()

        expected_dict = {
            "type": "token",
            "status": {"status": "OK", "reason": "00", "message": "", "date": None},
            "instrument": [{"keyword": "key1", "value": "value1", "displayOn": "none"}],
        }
        self.assertEqual(result_dict, expected_dict)

    def test_parse_instrument_empty_instrument(self):
        """
        Test parsing instrument when instrument list is empty.
        """
        subscription = SubscriptionInformation(type="account", instrument=[])
        result = subscription.parse_instrument()
        self.assertIsNone(result, "Expected None when instrument list is empty.")

    def test_empty_instrument_to_dict(self):
        """
        Test conversion to dictionary with an empty instrument list.
        """
        subscription = SubscriptionInformation(type="account")
        result_dict = subscription.to_dict()

        expected_dict = {
            "type": "account",
            "status": None,
            "instrument": [],
        }
        self.assertEqual(result_dict, expected_dict)

    def test_validate_instrument_none(self):
        """
        Test when instrument_data is None or empty.
        """
        result = SubscriptionInformation.validate_instrument(None)
        self.assertEqual(result, [])

    def test_validate_instrument_single_dict(self):
        """
        Test when instrument_data is a single dictionary.
        """
        data = {"keyword": "key1", "value": "value1"}
        result = SubscriptionInformation.validate_instrument(data)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], NameValuePair)
        self.assertEqual(result[0].keyword, "key1")
        self.assertEqual(result[0].value, "value1")

    def test_validate_instrument_list_of_dicts(self):
        """
        Test when instrument_data is a list of dictionaries.
        """
        data = [{"keyword": "key1", "value": "value1"}, {"keyword": "key2", "value": "value2"}]
        result = SubscriptionInformation.validate_instrument(data)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], NameValuePair)
        self.assertEqual(result[0].keyword, "key1")
        self.assertEqual(result[1].keyword, "key2")

    def test_validate_instrument_with_item_key(self):
        """
        Test when instrument_data contains an 'item' key with a list.
        """
        data = {"item": [{"keyword": "key1", "value": "value1"}, {"keyword": "key2", "value": "value2"}]}
        result = SubscriptionInformation.validate_instrument(data)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], NameValuePair)
        self.assertEqual(result[0].keyword, "key1")
        self.assertEqual(result[1].keyword, "key2")

    def test_validate_instrument_invalid_data(self):
        """
        Test when instrument_data is not a list or dict.
        """
        data = "invalid_data"
        with self.assertRaises(ValueError):
            SubscriptionInformation.validate_instrument(data)
