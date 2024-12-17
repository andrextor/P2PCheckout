from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    token: str = Field(default="", description="Unique token identifier")
    subtoken: str = Field(default="", description="Secondary token identifier")
    franchise: str = Field(default="", description="Franchise associated with the token")
    franchise_name: str = Field(default="", description="Name of the franchise", alias="franchiseName")
    issuer_name: str = Field(default="", description="Name of the issuer", alias="issuerName")
    last_digits: str = Field(default="", description="Last digits of the card/token", alias="lastDigits")
    valid_until: str = Field(default="", description="Expiration date in ISO format", alias="validUntil")
    cvv: str = Field(default="", description="CVV associated with the token")
    installments: Optional[int] = Field(default=None, description="Number of installments")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    def expiration(self) -> str:
        """
        Convert valid_until to 'mm/yy' format for expiration date.
        """
        try:
            expiration_date = datetime.strptime(self.valid_until, "%Y-%m-%d")
            return expiration_date.strftime("%m/%y")
        except ValueError:
            return "Invalid date"

    def to_dict(self) -> dict:
        """
        Convert the Token object to a dictionary using the Pydantic model_dump method.
        """
        return {
            "token": self.token,
            "subtoken": self.subtoken,
            "franchise": self.franchise,
            "franchiseName": self.franchise_name,
            "issuerName": self.issuer_name,
            "lastDigits": self.last_digits,
            "validUntil": self.valid_until,
            "cvv": self.cvv,
            "installments": self.installments,
        }
