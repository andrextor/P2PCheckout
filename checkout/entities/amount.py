from typing import List, Optional, Union

from pydantic import Field

from checkout.entities.amount_base import AmountBase
from checkout.entities.amount_detail import AmountDetail
from checkout.entities.tax_detail import TaxDetail


class Amount(AmountBase):
    taxes: List[TaxDetail] = Field(default_factory=list, description="List of tax details")
    details: List[AmountDetail] = Field(default_factory=list, description="List of amount details")
    tip: Optional[float] = Field(default=None, description="Optional tip amount")
    insurance: Optional[float] = Field(default=None, description="Optional insurance amount")

    def set_taxes(self, taxes: List[Union[dict, TaxDetail]]) -> None:
        """
        Set the taxes for the amount object.
        """
        self.taxes = [TaxDetail(**tax) if isinstance(tax, dict) else tax for tax in taxes]

    def set_details(self, details: List[Union[dict, AmountDetail]]) -> None:
        """
        Set the details for the amount object.
        """
        self.details = []
        for detail in details:
            if isinstance(detail, dict):
                detail = AmountDetail(**detail)
            self.details.append(detail)

    def taxes_to_dict(self) -> List[dict]:
        """
        Convert taxes to a list of dictionaries.
        """
        return [tax.model_dump() for tax in self.taxes]

    def details_to_dict(self) -> List[dict]:
        """
        Convert details to a list of dictionaries.
        """
        return [detail.model_dump() for detail in self.details]

    def to_dict(self) -> dict:
        """
        Convert the Amount object to a dictionary including taxes and details.
        """
        parent_data = super().to_dict()

        data = {
            **parent_data,
            "taxes": self.taxes_to_dict(),
            "details": self.details_to_dict(),
        }

        if self.tip is None:
            del data["tip"]
        if self.insurance is None:
            del data["insurance"]

        return data
