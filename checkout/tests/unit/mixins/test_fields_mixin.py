import unittest

from checkout.mixins.fields_mixin import FieldsMixin


class FieldsMixinTest(unittest.TestCase):

    def test_set_fields_with_dict(self):
        """
        Test setting fields with a dictionary containing an 'item' key.
        """
        mixin = FieldsMixin()
        fields_data = {"item": [{"keyword": "key1", "value": "value1"}, {"keyword": "key2", "value": "value2"}]}
        mixin.set_fields(fields_data)
        self.assertEqual(len(mixin.custom_fields), 2)
        self.assertEqual(mixin.custom_fields[0].keyword, "key1")
        self.assertEqual(mixin.custom_fields[1].keyword, "key2")
