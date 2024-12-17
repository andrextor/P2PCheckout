from typing import Dict, List, Optional, Union

from checkout.entities.name_value_pair import NameValuePair


class FieldsMixin:

    def get_fields(self) -> List[NameValuePair]:
        """
        Return the list of NameValuePair objects.
        """
        return self.custom_fields

    def set_fields(self, fields_data: Union[List[Dict], Dict]) -> None:
        """
        Set the fields based on the provided data.
        """
        if isinstance(fields_data, dict) and "item" in fields_data:
            fields_data = fields_data["item"]

        if not hasattr(self, "custom_fields"):
            self.custom_fields = []

        for nvp in fields_data:
            self.custom_fields.append(nvp if isinstance(nvp, NameValuePair) else NameValuePair(**nvp))

    def fields_to_array(self) -> List[Dict]:
        """
        Convert the fields to a list of dictionaries.
        """
        if not hasattr(self, "custom_fields"):
            self.custom_fields = []

        return [field.to_dict() for field in self.custom_fields if isinstance(field, NameValuePair)]

    def fields_to_key_value(self, nvps: Optional[List[NameValuePair]] = None) -> Dict[str, Union[str, list, dict]]:
        """
        Convert the fields to a key-value pair dictionary.
        """
        nvps_data = nvps if nvps is not None else self.custom_fields

        return {field.keyword: field.value for field in nvps_data if isinstance(field, NameValuePair)}

    def add_field(self, nvp: Union[Dict, NameValuePair]) -> None:
        """
        Add a new NameValuePair to the fields.
        """
        name_value_pair = nvp if isinstance(nvp, NameValuePair) else NameValuePair(**nvp)
        self.custom_fields.append(name_value_pair)
