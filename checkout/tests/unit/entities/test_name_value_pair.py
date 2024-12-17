import unittest

from checkout.entities.name_value_pair import NameValuePair
from checkout.enums.display_on_enum import DisplayOnEnum


class NameValuePairTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test initialization of NameValuePair with valid data.
        """
        pair = NameValuePair(keyword="testKey", value="testValue", display_on=DisplayOnEnum.BOTH)
        self.assertEqual(pair.keyword, "testKey")
        self.assertEqual(pair.value, "testValue")
        self.assertEqual(pair.display_on, DisplayOnEnum.BOTH)

    def test_default_values(self):
        """
        Test default values for optional fields.
        """
        pair = NameValuePair(keyword="defaultKey")
        self.assertEqual(pair.keyword, "defaultKey")
        self.assertIsNone(pair.value)
        self.assertEqual(pair.display_on, DisplayOnEnum.NONE)

    def test_to_dict(self):
        """
        Test conversion of NameValuePair to a dictionary.
        """
        pair = NameValuePair(keyword="testKey", value={"key": "value"}, display_on=DisplayOnEnum.RECEIPT)
        expected_dict = {
            "keyword": "testKey",
            "value": {"key": "value"},
            "displayOn": "receipt",
        }
        self.assertEqual(pair.to_dict(), expected_dict)

    def test_to_dict_exclude_none(self):
        """
        Test dictionary conversion with exclusion of None values.
        """
        pair = NameValuePair(keyword="testKey", display_on=DisplayOnEnum.PAYMENT)
        expected_dict = {"keyword": "testKey", "displayOn": "payment", "value": None}
        self.assertEqual(pair.to_dict(), expected_dict)

    def test_value_as_list(self):
        """
        Test initialization when value is a list.
        """
        pair = NameValuePair(keyword="testKey", value=["item1", "item2"])
        self.assertEqual(pair.value, ["item1", "item2"])

    def test_value_as_dict(self):
        """
        Test initialization when value is a dictionary.
        """
        pair = NameValuePair(keyword="testKey", value={"key": "value"})
        self.assertEqual(pair.value, {"key": "value"})
