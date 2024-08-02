from datetime import datetime
from capture.commands.capture_info import CaptureInfo
from capture.models import CapturedEvent
from django.contrib.auth.models import User
from django.utils import timezone


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
            # Parse the input date string
            date_obj = datetime.strptime(date_string, "%d/%m/%Y %H:%M")
            aware_date = timezone.make_aware(date_obj, timezone.get_current_timezone())
            # Format the date object to the required format
            return aware_date
        except ValueError as e:
            return f"Error: {str(e)}"

    
class CaptureEventAlreadyBroadcasted(Exception):
    """
    An exception to handle the case where a capture event has already been broadcasted.
    """