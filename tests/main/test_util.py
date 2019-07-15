from unittest import TestCase
from app.main.util import Config
import json


class ConfigTest(TestCase):
    def setUp(self):
        self.config = Config("tests/config.json")
        with open("tests/config.json", "r") as master_file:
            self.master_values = json.load(master_file)

    def test_with_existing_value(self):
        self.assertEqual(self.master_values["test"], self.config.test)

    def test_with_missing_value(self):
        with self.assertRaises(AttributeError):
            self.config.not_here
