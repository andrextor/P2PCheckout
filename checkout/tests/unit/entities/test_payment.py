import unittest

from checkout.entities.amount import Amount
from checkout.entities.discount import Discount
from checkout.entities.item import Item
from checkout.entities.name_value_pair import NameValuePair
from checkout.entities.payment import Payment
from checkout.entities.payment_modifier import PaymentModifier
from checkout.entities.person import Person
from checkout.entities.recurring import Recurring


class PaymentTest(unittest.TestCase):

    def test_payment_initialization(self):
        """
        Test the initialization of a Payment object with default values.
        """

        payment = Payment(reference="REF001", amount={"currency": "COP", "total": 10000})

        assert payment.reference == "REF001"
        assert payment.description == ""
        assert payment.amount.to_dict() == {"currency": "COP", "total": 10000.0, "taxes": [], "details": []}
        assert payment.allow_partial is False
        assert payment.shipping is None
        assert payment.items == []
        assert payment.recurring is None
        assert payment.discount is None
        assert payment.subscribe is False
        assert payment.agreement is None
        assert payment.agreement_type == ""
        assert payment.modifiers == []

    def test_payment_initialization_with_values(self):
        """
        Test the initialization of a Payment object with provided values.
        """
        amount = Amount(currency="USD", total=100.0)
        discount = Discount(code="DISC10", type="PERCENTAGE", amount=10.0, base=100.0)
        shipping = Person(document="123456789", name="John", surname="Doe")
        items = [Item(sku="ITEM001", name="Test Item", qty="1", price="50.0")]
        modifiers = [PaymentModifier(type="FEDERAL_GOVERNMENT", code="MOD001")]

        payment = Payment(
            reference="REF001",
            description="Test Payment",
            amount=amount,
            allow_partial=True,
            shipping=shipping,
            items=items,
            discount=discount,
            subscribe=True,
            agreement=123,
            agreement_type="TYPE001",
            modifiers=modifiers,
        )

        assert payment.reference == "REF001"
        assert payment.description == "Test Payment"
        assert payment.amount == amount
        assert payment.allow_partial is True
        assert payment.shipping == shipping
        assert payment.items == items
        assert payment.discount == discount
        assert payment.subscribe is True
        assert payment.agreement == 123
        assert payment.agreement_type == "TYPE001"
        assert payment.modifiers == modifiers

    def test_payment_initialization_with_recurring(self):
        """
        Test the initialization of a Payment object with dispersion values.
        """

        recurring_data = {
            "periodicity": "D",
            "interval": 1,
            "nextPayment": "2024-12-31",
            "maxPeriods": 2,
            "dueDate": "2025-01-01",
            "notificationUrl": "https://merchant.com/notification",
        }
        payment = Payment(
            reference="REF001",
            description="Test Payment",
            amount=Amount(currency="USD", total=100.0),
            recurring=Recurring(**recurring_data),
        )

        assert payment.to_dict()["recurring"] == recurring_data

    def test_set_items(self):
        """
        Test setting items in the Payment object.
        """
        payment = Payment(reference="REF001", amount={"currency": "COP", "total": 10000})
        items = [{"sku": "ITEM001", "name": "Test Item", "qty": "1", "price": "50.0"}]
        payment.set_items(items)

        assert len(payment.items) == 1
        assert payment.items[0].sku == "ITEM001"

    def test_items_to_array(self):
        """
        Test converting items to an array of dictionaries.
        """
        payment = Payment(reference="REF001", amount={"currency": "COP", "total": 10000})
        items = [{"sku": "ITEM001", "name": "Test Item", "qty": "1", "price": "50.0"}]
        payment.set_items(items)

        items_array = payment.items_to_array()
        assert len(items_array) == 1
        assert items_array[0]["sku"] == "ITEM001"

    def test_set_modifiers(self):
        """
        Test setting modifiers in the Payment object.
        """
        payment = Payment(reference="REF001", amount={"currency": "COP", "total": 10000})
        modifiers = [{"type": "CUSTOM_TYPE", "code": "MOD123"}]
        payment.set_modifiers(modifiers)

        assert len(payment.modifiers) == 1
        assert payment.modifiers[0].type == "CUSTOM_TYPE"

    def test_modifiers_to_array(self):
        """
        Test converting modifiers to an array of dictionaries.
        """
        payment = Payment(reference="REF001", amount={"currency": "COP", "total": 10000})
        modifiers = [{"type": "CUSTOM_TYPE", "code": "MOD123"}]
        payment.set_modifiers(modifiers)

        modifiers_array = payment.modifiers_to_array()
        assert len(modifiers_array) == 1
        assert modifiers_array[0]["type"] == "CUSTOM_TYPE"

    def test_to_dict(self):
        """
        Test converting the Payment object to a dictionary.
        """
        amount = Amount(currency="USD", total=100.0)
        discount = Discount(code="DISC10", type="PERCENTAGE", amount=10.0, base=100.0)
        shipping = Person(document="123456789", name="John", surname="Doe")
        items = [Item(sku="ITEM001", name="Test Item", qty="1", price="50.0")]
        modifiers = [PaymentModifier(type="FEDERAL_GOVERNMENT", code="MOD001")]

        payment = Payment(
            reference="REF001",
            description="Test Payment",
            amount=amount,
            shipping=shipping,
            items=items,
            discount=discount,
            agreement=123,
            agreement_type="TYPE001",
            modifiers=modifiers,
            custom_fields=[NameValuePair(keyword="field1", value="value1")],
        )

        payment.set_fields([NameValuePair(keyword="field2", value="value2")])
        payment_dict = payment.to_dict()
        fields = payment.get_fields()

        assert payment_dict["reference"] == "REF001"
        assert payment_dict["amount"]["currency"] == "USD"
        assert payment_dict["shipping"]["name"] == "John"
        assert payment_dict["items"][0]["sku"] == "ITEM001"
        assert payment_dict["discount"]["code"] == "DISC10"
        assert payment_dict["modifiers"][0]["type"] == "FEDERAL_GOVERNMENT"
        assert payment_dict["agreement"] == 123
        assert payment_dict["agreementType"] == "TYPE001"
        assert payment.fields_to_key_value() == {"field1": "value1", "field2": "value2"}
        assert fields[0].display_on == "none"
        assert fields[0].keyword == "field1"
        assert fields[0].value == "value1"
        assert fields[1].display_on == "none"
        assert fields[1].keyword == "field2"
        assert fields[1].value == "value2"
