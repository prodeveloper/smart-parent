from datetime import datetime
from capture.commands.capture_info import CaptureInfo
from capture.models import CapturedEvent
from django.contrib.auth.models import User
from django.utils import timezone
from dateutil import parser
from capture.commands.log_item import LogItem

class CaptureProcessedEvent:
    """
    A class to handle the processing of a capture event.
    """
    capture_info: CaptureInfo
    user: User
    broadcasted: bool = False
    def __init__(self, capture_info: CaptureInfo, user: User):
        self.capture_info = capture_info
        self.user = user
    
    def broadcast(self):
        if self.broadcasted:
            raise CaptureEventAlreadyBroadcasted("CaptureProcessedEvent already broadcasted")
        self._save_db()
        self.broadcasted = True
    
    def _save_db(self):
        for event in self.capture_info.parsed_events:
            CapturedEvent.objects.get_or_create(
                name=event['event'],
                description=event['description'],
                date_time=self._clean_date(event['date_time']),
                content_id=self.capture_info.uploaded_content.content_id,
                owner=self.user
            )

    def _clean_date(self, date_string):
        try:
            # Attempt to parse the date string
            date_obj = parser.parse(date_string)
            # If year is not 4 digits, assume it's day/month/year format
            if date_obj.year < 1000:
                date_obj = parser.parse(date_string, dayfirst=True)
            # Make the datetime aware
            aware_date = timezone.make_aware(date_obj, timezone.get_current_timezone())
            return aware_date
        except ValueError as exc:
            raise EventDateParseError(f"Error parsing date: {date_string}") from exc
    
class CaptureEventAlreadyBroadcasted(Exception):
    """
    An exception to handle the case where a capture event has already been broadcasted.
    """
class EventDateParseError(Exception):
    """
    An exception if we can't parse the date of the event.
    """