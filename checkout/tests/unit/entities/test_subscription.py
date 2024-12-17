import unittest

from checkout.entities.name_value_pair import NameValuePair
from checkout.entities.subscription import Subscription
from checkout.enums.display_on_enum import DisplayOnEnum


class SubscriptionTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test the initialization of a Subscription object.
        """
        subscription = Subscription(
            reference="SUB123",
            description="Test subscription",
            custom_fields=[
                NameValuePair(keyword="field1", value="value1"),
                NameValuePair(keyword="field2", value="value2"),
            ],
        )

        self.assertEqual(subscription.reference, "SUB123")
        self.assertEqual(subscription.description, "Test subscription")
        self.assertEqual(len(subscription.custom_fields), 2)
        self.assertEqual(subscription.custom_fields[0].keyword, "field1")
        self.assertEqual(subscription.custom_fields[0].value, "value1")

    def test_to_dict(self):
        """
        Test the to_dict method.
        """
        subscription = Subscription(
            reference="SUB123",
            description="Test subscription",
            custom_fields=[
                NameValuePair(keyword="field1", value="value1"),
                NameValuePair(keyword="field2", value="value2"),
            ],
        )

        expected_dict = {
            "reference": "SUB123",
            "description": "Test subscription",
            "fields": [
                {"keyword": "field1", "value": "value1", "displayOn": DisplayOnEnum.NONE},
                {"keyword": "field2", "value": "value2", "displayOn": DisplayOnEnum.NONE},
            ],
        }

        self.assertEqual(subscription.to_dict(), expected_dict)

    def test_empty_subscription(self):
        """
        Test the initialization of an empty Subscription object.
        """
        subscription = Subscription()
        self.assertEqual(subscription.reference, "")
        self.assertEqual(subscription.description, "")
        self.assertEqual(subscription.custom_fields, [])
        self.assertEqual(subscription.fields_to_array(), [])

    def test_fields_to_array(self):
        """
        Test the fields_to_array method from the FieldsMixin.
        """
        subscription = Subscription()
        subscription.add_field({"keyword": "key1", "value": "value1"})
        subscription.add_field({"keyword": "key2", "value": "value2"})

        expected_fields = [
            {"keyword": "key1", "value": "value1", "displayOn": DisplayOnEnum.NONE},
            {"keyword": "key2", "value": "value2", "displayOn": DisplayOnEnum.NONE},
        ]

        self.assertEqual(subscription.fields_to_array(), expected_fields)
