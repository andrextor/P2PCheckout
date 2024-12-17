from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from checkout.enums.display_on_enum import DisplayOnEnum


class NameValuePair(BaseModel):
    keyword: str = Field(..., description="The keyword associated with the value")
    value: Any = Field(default=None, description="The value, which can be a string, list, or dict")
    display_on: DisplayOnEnum = Field(
        default=DisplayOnEnum.NONE, description="Display setting for the keyword", alias="displayOn"
    )

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    def to_dict(self) -> dict:
        """
        Convert the NameValuePair object to a dictionary using the Pydantic `model_dump` method.
        """
        return {"keyword": self.keyword, "value": self.value, "displayOn": self.display_on.value}
