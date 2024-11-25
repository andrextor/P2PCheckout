from typing import List, Dict
from entities.payment import Payment


class DispersionPayment(Payment):
    dispersion: List[Payment] = []

    def __init__(self, data: Dict):
        """
        Initialize DispersionPayment object and process dispersion payments.
        """
        super().__init__(data)
        if "dispersion" in data:
            self.set_dispersion(data["dispersion"])

    def set_dispersion(self, data: List[Dict]) -> "DispersionPayment":
        """
        Set the dispersion payments.
        """
        self.dispersion = []
        for payment_data in data:
            payment = Payment(payment_data)
            payment.set_reference(self.reference).set_description(self.description)
            self.dispersion.append(payment)
        return self

    def dispersion_to_array(self) -> List[Dict]:
        """
        Convert the list of dispersion payments to a list of dictionaries.
        """
        return [payment.to_dict() for payment in self.dispersion]

    def to_dict(self) -> Dict:
        """
        Convert the DispersionPayment object to a dictionary.
        """
        base_data = super().to_dict()
        base_data["dispersion"] = self.dispersion_to_array()
        return base_data