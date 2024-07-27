from smartparent.config import ConfigLoader
from capture.models.local_firebase import FirebaseCache
from datetime import datetime

class EnforceLimitsCommand():
    text_to_enforce_limits_on:str = None
    text_no_times_run_today:int = 0

    def __init__(self, text_to_enforce_limits_on) -> None:
        self.text_to_enforce_limits_on = text_to_enforce_limits_on
    def run(self):
        if self.text_no_times_run_today is None:
            self.text_no_times_run_today = CheckLimitsCommand().get()
        if len(self.text_to_enforce_limits_on) > ConfigLoader().max_text_length():
            raise TextTooLongException
        if self.text_no_times_run_today >= ConfigLoader().max_times_run_today():
            raise TooManyTimesRunTodayException

class CheckLimitsCommand():
    def get(self,*,key=None):
        if key is None:
            key = "no_times_" + datetime.now().strftime("%Y-%m-%d")
        self.text_no_times_run_today = FirebaseCache().get(key)
        if self.text_no_times_run_today is None:
            self.text_no_times_run_today = 0
        FirebaseCache().set(key, self.text_no_times_run_today+1)
        return self.text_no_times_run_today
class TextTooLongException(Exception):
    pass

class TooManyTimesRunTodayException(Exception):
    pass