from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from checkout.entities.address import Address


class Person(BaseModel):
    document: str = Field(default="", description="Document number of the person")
    document_type: str = Field(default="", description="Type of document (e.g., ID, Passport)", alias="documentType")
    name: str = Field(default="", description="First name of the person")
    surname: str = Field(default="", description="Last name of the person")
    company: str = Field(default="", description="Company name if applicable")
    email: Optional[str] = Field(default="", description="Email address of the person")
    mobile: str = Field(default="", description="Mobile number of the person")
    address: Optional[Address] = Field(default=None, description="Address information")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    def is_business(self) -> bool:
        """
        Check if the person is representing a business based on their document type.
        """
        return bool(self.document_type and self._business_document(self.document_type))

    @staticmethod
    def _business_document(document_type: str) -> bool:
        """
        Placeholder for business document validation.
        Replace this with actual logic similar to DocumentHelper::businessDocument.
        """
        business_document_types = {"TIN", "VAT", "EIN"}
        return document_type in business_document_types

    def to_dict(self) -> dict:
        """
        Convert the person object to a dictionary using the new `model_dump` method.
        """

        return {
            "document": self.document,
            "documentType": self.document_type,
            "name": self.name,
            "surname": self.surname,
            "company": self.company,
            "email": self.email,
            "mobile": self.mobile,
            "address": self.address.to_dict() if self.address else "",
        }
