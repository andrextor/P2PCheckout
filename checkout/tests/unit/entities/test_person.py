import unittest

from checkout.entities.address import Address
from checkout.entities.person import Person


class PersonTest(unittest.TestCase):

    def test_person_initialization_with_defaults(self):
        """
        Test initialization with default values.
        """
        person = Person()

        assert person.document == ""
        assert person.document_type == ""
        assert person.name == ""
        assert person.surname == ""
        assert person.company == ""
        assert person.email == ""
        assert person.mobile == ""
        assert person.address is None

    def test_person_initialization_with_values(self):
        """
        Test initialization with provided values.
        """
        address = Address(
            street="123 Main St", city="Testville", state="TX", postal_code="12345", country="US", phone="123-456-7890"
        )

        person = Person(
            document="123456789",
            document_type="TIN",
            name="John",
            surname="Doe",
            company="TestCorp",
            email="john.doe@example.com",
            mobile="1234567890",
            address=address,
        )

        assert person.document == "123456789"
        assert person.document_type == "TIN"
        assert person.name == "John"
        assert person.surname == "Doe"
        assert person.company == "TestCorp"
        assert person.email == "john.doe@example.com"
        assert person.mobile == "1234567890"
        assert person.address == address

    def test_person_is_business(self):
        """
        Test the `is_business` method.
        """
        person_business = Person(documentType="TIN")
        person_non_business = Person(documentType="ID")

        assert person_business.is_business() is True
        assert person_non_business.is_business() is False

    def test_person_to_dict(self):
        """
        Test the `to_dict` method.
        """
        address = Address(
            street="123 Main St", city="Testville", state="TX", postal_code="12345", country="US", phone="123-456-7890"
        )

        person = Person(
            document="123456789",
            document_type="TIN",
            name="John",
            surname="Doe",
            company="TestCorp",
            email="john.doe@example.com",
            mobile="1234567890",
            address=address,
        )

        person_dict = person.to_dict()

        assert person_dict["document"] == "123456789"
        assert person_dict["documentType"] == "TIN"
        assert person_dict["name"] == "John"
        assert person_dict["surname"] == "Doe"
        assert person_dict["company"] == "TestCorp"
        assert person_dict["email"] == "john.doe@example.com"
        assert person_dict["mobile"] == "1234567890"
        assert person_dict["address"]["street"] == "123 Main St"

    def test_person_to_dict_without_address(self):
        """
        Test the `to_dict` method when address is not set.
        """
        person = Person(
            document="123456789",
            document_type="TIN",
            name="John",
            surname="Doe",
            company="TestCorp",
            email="john.doe@example.com",
            mobile="1234567890",
        )

        person_dict = person.to_dict()
        assert person_dict["document"] == "123456789"
        assert person_dict["documentType"] == "TIN"
        assert person_dict["name"] == "John"
        assert person_dict["surname"] == "Doe"
        assert person_dict["company"] == "TestCorp"
        assert person_dict["email"] == "john.doe@example.com"
        assert person_dict["mobile"] == "1234567890"
        assert person_dict["address"] == ""
