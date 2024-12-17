from pydantic import BaseModel, Field

from checkout.decorators.convert_to_boolean import convert_booleans_to_strings
from checkout.decorators.filter_empty_values import filter_empty_values
from checkout.entities.instrument import Instrument


class InvalidateToKenRequest(BaseModel):
    locale: str = Field(default="es_CO", description="Locale of the request")
    instrument: Instrument = Field(..., description="Instrument details")

    @filter_empty_values
    @convert_booleans_to_strings
    def to_dic(self) -> dict:
        return {"locale": self.locale, "instrument": self.instrument.to_dict()}
