from typing import Any, Dict, List, Union

from checkout.entities.payment import Payment


class DispersionPayment(Payment):
    dispersion: List[Payment] = []

    def __init__(self, **data: Dict[str, Any]):
        """
        Initialize DispersionPayment object and process dispersion payments.
        """
        payment_fields = self._extract_payment_fields(data)
        super().__init__(**payment_fields)
        if "dispersion" in data:
            self.set_dispersion(data["dispersion"])

    def _extract_payment_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and validate fields for initializing the base Payment class.
        """
        return {
            "reference": data.get("reference", ""),
            "description": data.get("description", ""),
            "amount": data.get("amount"),
            "allow_partial": data.get("allow_partial", False),
            "shipping": data.get("shipping"),
            "items": data.get("items", []),
            "recurring": data.get("recurring"),
            "payment": data.get("payment"),
            "discount": data.get("discount"),
            "subscribe": data.get("subscribe", False),
            "agreement": data.get("agreement"),
            "agreement_type": data.get("agreement_type", ""),
            "modifiers": data.get("modifiers", []),
            "custom_fields": data.get("custom_fields", []),
        }

    def set_dispersion(self, data: Union[List[Dict], Dict]) -> "DispersionPayment":
        """
        Set the dispersion payments.
        """
        self.dispersion = []
        for payment_data in data:
            payment = Payment(**payment_data) if isinstance(payment_data, dict) else payment_data
            self.dispersion.append(payment)
        return self

    def dispersion_to_dict(self) -> List[Dict]:
        """
        Convert the list of dispersion payments to a list of dictionaries.
        """
        return [payment.to_dict() for payment in self.dispersion]

    def to_dict(self) -> Dict:
        """
        Convert the DispersionPayment object to a dictionary.
        """
        base_data = super().to_dict()
        base_data["dispersion"] = self.dispersion_to_dict()
        return base_data
