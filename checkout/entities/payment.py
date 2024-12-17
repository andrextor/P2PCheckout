from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from checkout.entities.amount import Amount
from checkout.entities.discount import Discount
from checkout.entities.item import Item
from checkout.entities.name_value_pair import NameValuePair
from checkout.entities.payment_modifier import PaymentModifier
from checkout.entities.person import Person
from checkout.entities.recurring import Recurring
from checkout.mixins.fields_mixin import FieldsMixin


class Payment(BaseModel, FieldsMixin):
    reference: str = Field(..., description="Payment reference")
    description: str = Field(default="", description="Description of the payment")
    amount: Amount = Field(default=..., description="Amount information")
    allow_partial: bool = Field(default=False, description="Allow partial payments", alias="allowPartial")
    shipping: Optional[Person] = Field(default=None, description="Shipping details")
    items: List[Item] = Field(default_factory=list, description="List of items")
    recurring: Optional[Recurring] = Field(default=None, description="Recurring payment details")
    discount: Optional[Discount] = Field(default=None, description="Discount information")
    subscribe: bool = Field(default=False, description="Subscribe flag")
    agreement: Optional[int] = Field(default=None, description="Agreement ID")
    agreement_type: str = Field(default="", description="Type of agreement", alias="agreementType")
    modifiers: List[PaymentModifier] = Field(default_factory=list, description="List of payment modifiers")
    custom_fields: List[NameValuePair] = Field(default=[], description="Additional fields for the payment")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    def set_items(self, items: Union[List[dict], List[Item]]) -> None:
        """
        Set the items for the payment.
        """
        self.items = [Item(**item) if isinstance(item, dict) else item for item in items]

    def items_to_array(self) -> List[dict]:
        """
        Convert the items list to an array of dictionaries.
        """
        return [item.model_dump() for item in self.items]

    def set_modifiers(self, modifiers: Union[List[dict], List[PaymentModifier]]) -> None:
        """
        Set the payment modifiers.
        """
        self.modifiers = [PaymentModifier(**mod) if isinstance(mod, dict) else mod for mod in modifiers]

    def modifiers_to_array(self) -> List[dict]:
        """
        Convert the modifiers list to an array of dictionaries.
        """
        return [modifier.model_dump() for modifier in self.modifiers]

    def to_dict(self) -> dict:
        """
        Convert the Payment object to a dictionary, including nested objects.
        """
        data = {
            "reference": self.reference,
            "description": self.description,
            "amount": self.amount.to_dict(),
            "allowPartial": self.allow_partial,
            "items": self.items_to_array(),
            "subscribe": self.subscribe,
            "modifiers": self.modifiers_to_array(),
            "fields": self.fields_to_array(),
        }

        if self.shipping:
            data["shipping"] = self.shipping.to_dict()
        if self.recurring:
            data["recurring"] = self.recurring.to_dict()
        if self.discount:
            data["discount"] = self.discount.to_dict()
        if self.agreement:
            data["agreement"] = self.agreement
        if self.agreement_type:
            data["agreementType"] = self.agreement_type

        return data
