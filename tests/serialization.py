import unittest
import json
import pydantic
import datetime
from src.serializers.input import InputJsonDatabaseConnector, InputJsonSerializer


class TestSerialization(unittest.TestCase):

    def setUp(self) -> None:
        with open('datasets/correct_input.json', 'r') as f:
            self.correct_input_json = json.load(f)

    def test_correct_serializing(self):
        """
        Pydantic BaseModel will raise ValidationError if mistakes
        """
        InputJsonSerializer(**self.correct_input_json)

    def test_broken_created_input_datetime(self):
        """
        Raise if created datetime isn't datetime convertible string
        """
        self.local_json = self.correct_input_json
        self.local_json["created"] = "202-25T16:25:21+00:00"
        with self.assertRaises(pydantic.ValidationError):
            InputJsonSerializer(**self.correct_input_json)

    def test_broken_updated_input_datetime(self):
        """
        Raise if updated datetime isn't datetime convertible string
        """
        self.local_json = self.correct_input_json
        self.local_json["updated"] = "202-25T16:25:21+00:00"
        with self.assertRaises(pydantic.ValidationError):
            InputJsonSerializer(**self.correct_input_json)

    def test_is_string_time_converted_to_dt(self):
        """
        Datetimes must convert to datetime objects after serialization
        """
        serializer = InputJsonSerializer(**self.correct_input_json)
        self.assertIsInstance(serializer.created, datetime.datetime)
        self.assertIsInstance(serializer.updated, datetime.datetime)

    def test_database_connector_with_correct_data(self):
        """
        Check for general Exceptions
        """
        serializer = InputJsonSerializer(**self.correct_input_json)
        InputJsonDatabaseConnector(serializer)

    def test_database_connector_counters_sum(self):
        """
        Check for correct summ
        """
        serializer = InputJsonSerializer(**self.correct_input_json)
        obj = InputJsonDatabaseConnector(serializer)
        sum = obj.counters_total
        self.assertEqual(sum, 3)
        with self.assertRaises(AssertionError):
            self.assertEqual(sum, 5)
