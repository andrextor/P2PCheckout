from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from checkout.decorators.convert_to_boolean import convert_booleans_to_strings
from checkout.decorators.filter_empty_values import filter_empty_values
from checkout.entities.dispersion_payment import DispersionPayment
from checkout.entities.name_value_pair import NameValuePair
from checkout.entities.person import Person
from checkout.entities.subscription import Subscription
from checkout.mixins.fields_mixin import FieldsMixin


class RedirectRequest(BaseModel, FieldsMixin):

    locale: str = Field(default="es_CO", description="Locale of the request")
    payer: Optional[Person] = Field(default=None, description="Information about the payer")
    buyer: Optional[Person] = Field(default=None, description="Information about the buyer")
    payment: Optional[DispersionPayment] = Field(default=None, description="Payment details")
    subscription: Optional[Subscription] = Field(default=None, description="Subscription details")
    return_url: str = Field(..., description="URL to return to after processing", alias="returnUrl")
    payment_method: Optional[str] = Field(default=None, description="Payment method to be used", alias="paymentMethod")
    cancel_url: Optional[str] = Field(default=None, description="URL to return to if canceled", alias="cancelUrl")
    ip_address: str = Field(..., description="IP address of the user", alias="ipAddress")
    user_agent: str = Field(..., description="User agent of the user's browser", alias="userAgent")
    expiration: Optional[str] = Field(default=None, description="Expiration date for the request")
    capture_address: bool = Field(default=False, description="Whether to capture the address", alias="captureAddress")
    skip_result: bool = Field(default=False, description="Whether to skip showing results", alias="skipResult")
    no_buyer_fill: bool = Field(
        default=False, description="Whether to avoid pre-filling buyer data", alias="noBuyerFill"
    )
    custom_fields: List[NameValuePair] = Field(default=[], description="Additional fields for the redirect_request")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @filter_empty_values
    @convert_booleans_to_strings
    def to_dict(self) -> dict:
        """
        Convert the RedirectRequest object to a dictionary using Pydantic's dict method.
        """

        return {
            "locale": self.locale,
            "payer": self.payer.to_dict() if self.payer else "",
            "buyer": self.buyer.to_dict() if self.buyer else "",
            "payment": self.payment.to_dict() if self.payment else "",
            "subscription": self.subscription.to_dict() if self.subscription else "",
            "returnUrl": self.return_url,
            "payment_method": self.payment_method,
            "cancelUrl": self.cancel_url,
            "ipAddress": self.ip_address,
            "userAgent": self.user_agent,
            "expiration": self.expiration,
            "captureAddress": self.capture_address,
            "skipResult": self.skip_result,
            "noBuyerFill": self.no_buyer_fill,
            "fields": self.fields_to_array(),
        }
