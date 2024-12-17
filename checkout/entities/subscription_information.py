from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from checkout.entities.account import Account
from checkout.entities.name_value_pair import NameValuePair
from checkout.entities.status import Status
from checkout.entities.token import Token


class SubscriptionInformation(BaseModel):
    type: str = Field(default="", description="Type of subscription (e.g., token, account)")
    status: Optional[Status] = Field(default=None, description="Status information")
    instrument: List[NameValuePair] = Field(default_factory=list, description="Instrument details as name-value pairs")

    @field_validator("instrument", mode="before")
    @classmethod
    def validate_instrument(
        cls, instrument_data: Union[List[dict], List[NameValuePair], dict, None]
    ) -> List[NameValuePair]:
        """
        Ensure the instrument field is always a list of NameValuePair objects.
        """
        if not instrument_data:
            return []

        if isinstance(instrument_data, dict):
            if "item" in instrument_data:
                instrument_data = instrument_data["item"]
            else:
                instrument_data = [instrument_data]

        if not isinstance(instrument_data, list):
            raise ValueError("Instrument data must be a list of dictionaries or NameValuePair objects.")

        return [nvp if isinstance(nvp, NameValuePair) else NameValuePair(**nvp) for nvp in instrument_data]

    def set_instrument(self, instrument_data: Union[dict, List[dict]]) -> None:
        """
        Set the instrument data as a list of NameValuePair objects.
        """
        self.instrument = []
        if isinstance(instrument_data, dict) and "item" in instrument_data:
            instrument_data = instrument_data["item"]

        for nvp_data in instrument_data:
            nvp_data = nvp_data if isinstance(nvp_data, NameValuePair) else NameValuePair(**nvp_data)
            self.instrument.append(nvp_data)

    def instrument_to_list(self) -> List[dict]:
        """
        Convert the instrument to a list of dictionaries.
        """
        return [nvp.to_dict() for nvp in self.instrument]

    def parse_instrument(self) -> Optional[Union[Account, Token]]:
        """
        Parse the instrument as the proper entity (Account or Token) or return None.
        """
        if not self.instrument:
            return None

        data: Dict[str, Any] = {}
        if self.status:
            data["status"] = self.status

        for nvp in self.instrument:
            data[nvp.keyword] = nvp.value

        if self.type == "token":
            return Token(**data)

        elif self.type == "account":
            return Account(
                bankCode=data.get("bankCode", ""),
                bankName=data.get("bankName", ""),
                accountType=data.get("accountType", ""),
                accountNumber=data.get("accountNumber", ""),
                status=self.status if isinstance(self.status, Status) else None,
            )

        return None

    def to_dict(self) -> dict:
        """
        Convert the SubscriptionInformation object to a dictionary.
        """
        return {
            "type": self.type,
            "status": self.status.to_dict() if self.status else None,
            "instrument": self.instrument_to_list(),
        }
