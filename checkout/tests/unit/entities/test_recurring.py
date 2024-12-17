import unittest

from checkout.entities.recurring import Recurring


class RecurringTest(unittest.TestCase):

    def test_recurring_initialization_with_defaults(self):
        """
        Test initialization with default values.
        """
        recurring = Recurring(
            periodicity="M",
            interval=1,
            next_payment="2024-01-01",
        )

        assert recurring.periodicity == "M"
        assert recurring.interval == 1
        assert recurring.next_payment == "2024-01-01"
        assert recurring.max_periods == -1
        assert recurring.due_date == ""
        assert recurring.notification_url == ""

    def test_recurring_initialization_with_values(self):
        """
        Test initialization with all values provided.
        """
        recurring = Recurring(
            periodicity="M",
            interval=1,
            next_payment="2024-01-01",
            max_periods=12,
            due_date="2024-12-31",
            notification_url="https://example.com/notify",
        )

        assert recurring.periodicity == "M"
        assert recurring.interval == 1
        assert recurring.next_payment == "2024-01-01"
        assert recurring.max_periods == 12
        assert recurring.due_date == "2024-12-31"
        assert recurring.notification_url == "https://example.com/notify"

    def test_recurring_to_dict(self):
        """
        Test the `to_dict` method.
        """
        recurring = Recurring(
            periodicity="M",
            interval=1,
            next_payment="2024-01-01",
            max_periods=12,
            due_date="2024-12-31",
            notification_url="https://example.com/notify",
        )

        recurring_dict = recurring.to_dict()

        expected_dict = {
            "periodicity": "M",
            "interval": 1,
            "nextPayment": "2024-01-01",
            "maxPeriods": 12,
            "dueDate": "2024-12-31",
            "notificationUrl": "https://example.com/notify",
        }

        assert recurring_dict == expected_dict

    def test_recurring_to_dict_exclude_defaults(self):
        """
        Test the `to_dict` method when optional fields are not set.
        """
        recurring = Recurring(
            periodicity="D",
            interval=7,
            next_payment="2024-01-01",
        )

        recurring_dict = recurring.to_dict()

        expected_dict = {
            "periodicity": "D",
            "interval": 7,
            "nextPayment": "2024-01-01",
            "maxPeriods": -1,
            "dueDate": "",
            "notificationUrl": "",
        }

        assert recurring_dict == expected_dict
