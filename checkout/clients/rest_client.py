from typing import Dict

from checkout.contracts.carrier import Carrier
from checkout.entities.settings import Settings
from checkout.entities.status import Status
from checkout.messages.requests.collect import CollectRequest
from checkout.messages.requests.invalidate_token import InvalidateToKenRequest
from checkout.messages.requests.redirect import RedirectRequest
from checkout.messages.responses.information import InformationResponse
from checkout.messages.responses.redirect import RedirectResponse
from checkout.messages.responses.reverse import ReverseResponse


class RestCarrier(Carrier):
    def __init__(self, settings: Settings):
        """
        Initialize the RestCarrier with the given settings.

        :param settings: Settings object with client, authentication, base URL, and logger.
        """
        self.settings = settings

    def _post(self, endpoint: str, arguments: Dict) -> Dict:
        """
        Make an HTTP POST request using the HttpClient.

        :param endpoint: API endpoint.
        :param arguments: Request data.
        :return: Response as a dictionary.
        """
        data = {**arguments, "auth": self.settings.authentication().to_dict()}
        return self.settings.get_client().post(endpoint=endpoint, json=data, headers=self.settings.headers)

    def request(self, redirect_request: RedirectRequest) -> RedirectResponse:
        """
        Handle a redirect request.
        """
        result = self._post("api/session", redirect_request.to_dict())
        return RedirectResponse(**result)

    def query(self, request_id: str) -> InformationResponse:
        """
        Query a session by request ID.
        """
        result = self._post(f"api/session/{request_id}", {})
        return InformationResponse(**result)

    def collect(self, collect_request: CollectRequest) -> InformationResponse:
        """
        Handle a collect request.
        """
        result = self._post("api/collect", collect_request.to_dict())
        return InformationResponse(**result)

    def reverse(self, transaction_id: str) -> ReverseResponse:
        """
        Reverse a transaction.
        """
        result = self._post("api/reverse", {"internalReference": transaction_id})
        return ReverseResponse(**result)

    def invalidateToken(self, invalidate_token_request: InvalidateToKenRequest) -> Status:
        """
        Invalidate a token.
        """
        result = self._post("/api/instrument/invalidate", invalidate_token_request.to_dic())

        return Status.from_dict(result)
