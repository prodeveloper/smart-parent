from capture.services.validators import PreFlightValidator, TextLengthError, GeminiKeyError
import pytest
from django.test import TestCase
from capture.commands.enforce_limits import EnforceLimitsCommand, TextTooLongException,TooManyTimesRunTodayException, CheckLimitsCommand
from smartparent.config import ConfigLoader
class TestValidators(TestCase):
    """
    Test the validators.
    """
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
        with pytest.raises(GeminiKeyError):
            validator.key_error(key)
    def test_enforce_limits(self):
        text = "This is a test"*10000
        enforce_limits_command = EnforceLimitsCommand(text)
        with pytest.raises(TextTooLongException):
            enforce_limits_command.run()
    def test_too_many_times_run(self):
        text = "This is a test"
        enforce_limits_command = EnforceLimitsCommand(text)
        enforce_limits_command.text_no_times_run_today = ConfigLoader().throttle_config.MAX_TIMES_PER_DAY
        with pytest.raises(TooManyTimesRunTodayException):
            enforce_limits_command.run()
        within_limits_command = EnforceLimitsCommand(text)
        within_limits_command.text_no_times_run_today = ConfigLoader().throttle_config.MAX_TIMES_PER_DAY - 1
        within_limits_command.run()


