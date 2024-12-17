from typing import List

from pydantic import BaseModel, ConfigDict, Field

from checkout.entities.name_value_pair import NameValuePair
from checkout.mixins.fields_mixin import FieldsMixin


class Subscription(BaseModel, FieldsMixin):
    reference: str = Field(default="", description="Reference for the subscription")
    description: str = Field(default="", description="Description of the subscription")
    custom_fields: List[NameValuePair] = Field(default=[], description="Additional fields for the subscription")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    def to_dict(self) -> dict:
        """
        Convert the subscription object to a dictionary including fields.
        """
        data = self.model_dump()
        data["fields"] = self.fields_to_array()
        del data["custom_fields"]

        return data
