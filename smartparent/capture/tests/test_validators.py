from capture.services.validators import PreFlightValidator, TextLengthError, KeyError
import pytest
from django.test import TestCase

class TestValidators(TestCase):
    def test_text_length(self):
        validator = PreFlightValidator()
        validator.text_length("This is a test")
    def test_long_text_length(self):
        validator = PreFlightValidator()
        with pytest.raises(TextLengthError):
            validator.text_length("This is a test"*10000)
    def test_invalid_key(self):
        validator = PreFlightValidator()
        key = "some randon key"
        with pytest.raises(KeyError):
            validator.key_error(key)
