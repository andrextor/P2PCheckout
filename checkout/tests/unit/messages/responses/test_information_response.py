import unittest

from checkout.entities.status import Status
from checkout.entities.subscription_information import SubscriptionInformation
from checkout.entities.transaction import Transaction
from checkout.enums.status_enum import StatusEnum
from checkout.messages.requests.redirect import RedirectRequest
from checkout.messages.responses.information import InformationResponse


class InformationTest(unittest.TestCase):

    def test_initialization_with_all_fields(self):
        """
        Test initialization of Information with all fields provided.
        """
        status = Status(status=StatusEnum.OK, reason="Request successful")
        request = RedirectRequest(
            locale="en_US",
            return_url="https://example.com/return",
            ip_address="192.168.0.1",
            user_agent="TestAgent",
        )
        transaction = Transaction(
            reference="REF001",
            internal_reference="INT001",
            payment_method="CreditCard",
            payment_method_name="Visa",
            issuer_name="Bank A",
            authorization="AUTH001",
            receipt="REC001",
            franchise="VISA",
            refunded=False,
        )
        subscription = SubscriptionInformation(type="token")

        information = InformationResponse(
            request_id="REQ123",
            status=status,
            request=request,
            payment=[transaction],
            subscription=subscription,
        )

        self.assertEqual(information.request_id, "REQ123")
        self.assertEqual(information.status.reason, "Request successful")
        self.assertEqual(information.request.return_url, "https://example.com/return")
        self.assertEqual(len(information.payment), 1)
        self.assertEqual(information.subscription.type, "token")

    def test_initialization_with_defaults(self):
        """
        Test initialization of Information with default values.
        """
        information = InformationResponse(request_id="REQ123")

        self.assertEqual(information.request_id, "REQ123")
        self.assertIsNone(information.status)
        self.assertIsNone(information.request)
        self.assertIsNone(information.payment)
        self.assertIsNone(information.subscription)

    def test_set_payment(self):
        """
        Test setting payment transactions.
        """
        payments_data = [
            {"reference": "REF001", "internalReference": "INT001", "authorization": "AUTH001"},
            {"reference": "REF002", "internalReference": "INT002", "authorization": "AUTH002"},
        ]

        information = InformationResponse(request_id="REQ123")
        information.set_payment(payments_data)

        self.assertEqual(len(information.payment), 2)
        self.assertEqual(information.payment[0].reference, "REF001")
        self.assertEqual(information.payment[1].reference, "REF002")

    def test_last_transaction(self):
        """
        Test retrieving the last transaction.
        """
        transaction1 = Transaction(reference="REF001", authorization="AUTH001", refunded=False)
        transaction2 = Transaction(reference="REF002", authorization="AUTH002", refunded=False)

        information = InformationResponse(request_id="REQ123", payment=[transaction1, transaction2])

        last_transaction = information.last_transaction()
        self.assertEqual(last_transaction.reference, "REF002")

    def test_last_approved_transaction(self):
        """
        Test retrieving the last approved transaction.
        """
        status_approved = Status(status=StatusEnum.APPROVED, reason="Approved")
        transaction1 = Transaction(reference="REF001", authorization="AUTH001", refunded=False)
        transaction2 = Transaction(reference="REF002", authorization="AUTH002", refunded=False, status=status_approved)

        information = InformationResponse(request_id="REQ123", payment=[transaction1, transaction2])

        last_approved_transaction = information.last_approved_transaction()
        self.assertEqual(last_approved_transaction.reference, "REF002")

    def test_last_authorization(self):
        """
        Test retrieving the last authorization.
        """
        status_approved = Status(status=StatusEnum.APPROVED, reason="Approved")
        transaction = Transaction(reference="REF001", authorization="AUTH001", refunded=False, status=status_approved)

        information = InformationResponse(request_id="REQ123", payment=[transaction])

        last_authorization = information.last_authorization()
        self.assertEqual(last_authorization, "AUTH001")

    def test_to_dict(self):
        """
        Test converting the Information object to a dictionary.
        """
        status = Status(status=StatusEnum.OK, reason="Request successful")
        transaction = Transaction(reference="REF001", authorization="AUTH001")
        subscription = SubscriptionInformation(type="token")

        information = InformationResponse(
            request_id="REQ123",
            status=status,
            payment=[transaction],
            subscription=subscription,
        )

        expected_dict = {
            "requestId": "REQ123",
            "status": status.to_dict(),
            "request": None,
            "payment": [transaction.to_dict()],
            "subscription": subscription.to_dict(),
        }

        self.assertEqual(information.to_dict(), expected_dict)

    def test_set_payment_with_nested_transactions(self):
        """
        Test `set_payment` when the input contains nested transactions in a dictionary.
        """
        information = InformationResponse(
            request_id="12345",
            status=Status(status="OK", reason="Success"),
        )
        nested_payments = {
            "transaction": [
                {"reference": "TX001", "amount": {"currency": "USD", "total": 100}},
                {"reference": "TX002", "amount": {"currency": "USD", "total": 200}},
            ]
        }
        information.set_payment(nested_payments)
        self.assertEqual(len(information.payment), 2)
        self.assertEqual(information.payment[0].reference, "TX001")
        self.assertEqual(information.payment[1].reference, "TX002")

    def test_last_transaction_no_payments(self):
        """
        Test `last_transaction` when there are no payments.
        """
        information = InformationResponse(
            request_id="12345",
            status=Status(status="OK", reason="Success"),
        )
        self.assertIsNone(information.last_transaction())

    def test_set_payment_with_empty_list(self):
        """
        Test `set_payment` when the input is an empty list.
        """
        information = InformationResponse(
            request_id="12345",
            status=Status(status="OK", reason="Success"),
        )
        information.set_payment([])
        self.assertIsNone(information.payment)

    def test_last_transaction_no_approved(self):
        """
        Test `last_transaction` when `approved=True` and no transactions are approved.
        """
        information = InformationResponse(
            request_id="12345",
            status=Status(status=StatusEnum.OK, reason="Success"),
            payment=[
                Transaction(reference="TX001", status=Status(status=StatusEnum.FAILED, reason="Failed")),
                Transaction(reference="TX002", status=Status(status=StatusEnum.FAILED, reason="Failed")),
            ],
        )

        self.assertIsNone(information.last_transaction(approved=True))
