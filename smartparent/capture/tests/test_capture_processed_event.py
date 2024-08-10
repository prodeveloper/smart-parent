from django.test import TestCase
from capture.events.capture_processed import CaptureProcessedEvent, EventDateParseError
from django.contrib.auth.models import User
from capture.commands.capture_info import CaptureInfo
from capture.data_types.uploaded import UploadedContent
from capture.models import CapturedEvent
from capture.commands.log_item import LogItem

class TestCaptureProcessedEvent(TestCase):
    def test_capture_processed_event(self):
        uploaded_content = UploadedContent(content_id="test_content_id", content="test_content")
        capture_info = CaptureInfo(uploaded_content=uploaded_content)
        capture_info.parsed_events = [
            {
                "event": "test_event",
                "description": "test_description",
                "date_time": "01/09/2022 00:00"
            }
        ]
        user = User.objects.create_user(username="test_user", password="test_password")
        captured_event = CaptureProcessedEvent(capture_info=capture_info, user=user)
        captured_event.broadcast()
        #test initiated properly
        self.assertEqual(captured_event.capture_info, capture_info)
        self.assertEqual(captured_event.user, user)
        saved_events = CapturedEvent.objects.filter(content_id=uploaded_content.content_id)
        #test we actually saved the events
        self.assertEqual(saved_events.count(), 1)
        self.assertEqual(saved_events[0].name, "test_event")
        self.assertEqual(saved_events[0].description, "test_description")
        self.assertEqual(saved_events[0].owner, user)
    
    def test_capture_processed_event_date_parse_error(self):
        date_string = "not a date"
        captured_event = CaptureProcessedEvent(capture_info=None, user=None)
        with self.assertRaises(EventDateParseError):
            captured_event._clean_date(date_string)
