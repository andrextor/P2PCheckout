import unittest

from checkout.entities.amount import Amount
from checkout.entities.dispersion_payment import DispersionPayment
from checkout.entities.payment import Payment


class DispersionPaymentTest(unittest.TestCase):

    def test_dispersion_payment_initialization(self):

        data = {
            "reference": "REF001",
            "description": "Main Payment",
            "amount": {"currency": "USD", "total": 100.0},
            "dispersion": [
                Payment(reference="DISP001", description="Split Payment 1", amount=Amount(total=1000, currency="COP")),
                {
                    "reference": "DISP002",
                    "description": "Split Payment 2",
                    "amount": {"currency": "COP", "total": 1000},
                },
            ],
        }

        dispersion_payment = DispersionPayment(**data)

        self.assertEqual(dispersion_payment.reference, "REF001")
        self.assertEqual(dispersion_payment.description, "Main Payment")
        self.assertEqual(len(dispersion_payment.dispersion), 2)

        self.assertEqual(dispersion_payment.dispersion[0].reference, "DISP001")
        self.assertEqual(dispersion_payment.dispersion[0].description, "Split Payment 1")
        self.assertEqual(dispersion_payment.dispersion[0].amount.total, 1000.0)

        self.assertEqual(dispersion_payment.dispersion[1].reference, "DISP002")
        self.assertEqual(dispersion_payment.dispersion[1].description, "Split Payment 2")
        self.assertEqual(dispersion_payment.dispersion[1].amount.total, 1000.0)

    def test_set_dispersion(self):
        """
        Test setting dispersion payments after initialization.
        """
        data = {
            "reference": "REF001",
            "description": "Main Payment",
            "amount": {"currency": "USD", "total": 100.0},
        }

        dispersion_payment = DispersionPayment(**data)

        dispersion_data = [
            {"reference": "DISP001", "description": "Split Payment 1", "amount": {"currency": "USD", "total": 50.0}},
            {"reference": "DISP002", "description": "Split Payment 2", "amount": {"currency": "USD", "total": 50.0}},
        ]

        dispersion_payment.set_dispersion(dispersion_data)

        self.assertEqual(len(dispersion_payment.dispersion), 2)
        self.assertEqual(dispersion_payment.dispersion[0].reference, "DISP001")
        self.assertEqual(dispersion_payment.dispersion[1].reference, "DISP002")

    def test_dispersion_to_dict(self):
        """
        Test converting the dispersion payments to a dictionary.
        """
        data = {
            "reference": "REF001",
            "description": "Main Payment",
            "amount": {"currency": "USD", "total": 100.0},
            "dispersion": [
                {
                    "reference": "DISP001",
                    "description": "Split Payment 1",
                    "amount": {"currency": "USD", "total": 50.0},
                },
                {
                    "reference": "DISP002",
                    "description": "Split Payment 2",
                    "amount": {"currency": "USD", "total": 50.0},
                },
            ],
        }

        dispersion_payment = DispersionPayment(**data)

        expected_dispersion = [
            {
                "reference": "DISP001",
                "description": "Split Payment 1",
                "allowPartial": False,
                "items": [],
                "subscribe": False,
                "modifiers": [],
                "fields": [],
                "amount": {"currency": "USD", "total": 50.0, "taxes": [], "details": []},
            },
            {
                "reference": "DISP002",
                "description": "Split Payment 2",
                "allowPartial": False,
                "items": [],
                "subscribe": False,
                "modifiers": [],
                "fields": [],
                "amount": {"currency": "USD", "total": 50.0, "taxes": [], "details": []},
            },
        ]

        self.assertEqual(dispersion_payment.dispersion_to_dict(), expected_dispersion)

    def test_dispersion_payment_to_dict(self):
        """
        Test converting the entire DispersionPayment object to a dictionary.
        """
        data = {
            "reference": "REF001",
            "description": "Main Payment",
            "amount": {"currency": "USD", "total": 100.0},
            "dispersion": [
                {
                    "reference": "DISP001",
                    "description": "Split Payment 1",
                    "amount": {"currency": "USD", "total": 50.0},
                },
                {
                    "reference": "DISP002",
                    "description": "Split Payment 2",
                    "amount": {"currency": "USD", "total": 50.0},
                },
            ],
        }

        dispersion_payment = DispersionPayment(**data)

        expected_dict = {
            "reference": "REF001",
            "description": "Main Payment",
            "allowPartial": False,
            "items": [],
            "subscribe": False,
            "modifiers": [],
            "fields": [],
            "amount": {"currency": "USD", "total": 100.0, "taxes": [], "details": []},
            "dispersion": [
                {
                    "reference": "DISP001",
                    "description": "Split Payment 1",
                    "allowPartial": False,
                    "items": [],
                    "subscribe": False,
                    "modifiers": [],
                    "fields": [],
                    "amount": {"currency": "USD", "total": 50.0, "taxes": [], "details": []},
                },
                {
                    "reference": "DISP002",
                    "description": "Split Payment 2",
                    "allowPartial": False,
                    "items": [],
                    "subscribe": False,
                    "modifiers": [],
                    "fields": [],
                    "amount": {"currency": "USD", "total": 50.0, "taxes": [], "details": []},
                },
            ],
        }

        self.assertEqual(dispersion_payment.to_dict(), expected_dict)
