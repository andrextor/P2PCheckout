from typing import Protocol

from checkout.entities.status import Status
from checkout.messages.requests.collect import CollectRequest
from checkout.messages.requests.invalidate_token import InvalidateToKenRequest
from checkout.messages.requests.redirect import RedirectRequest
from checkout.messages.responses.information import InformationResponse
from checkout.messages.responses.redirect import RedirectResponse
from checkout.messages.responses.reverse import ReverseResponse


class Carrier(Protocol):
    def request(self, redirect_request: RedirectRequest) -> RedirectResponse:
        """
        Handle a redirect request.
        """

    def query(self, request_id: str) -> InformationResponse:
        """
        Query a redirect by request ID.
        """

    def collect(self, collect_request: CollectRequest) -> InformationResponse:
        """
        Collect redirect information from a request.
        """

    def reverse(self, transaction_id: str) -> ReverseResponse:
        """
        Reverse a transaction by its ID.
        """

    def invalidateToken(self, invalidate_token_request: InvalidateToKenRequest) -> Status:
        """
        invalidate a token.
        """
