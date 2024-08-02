from capture.commands.capture_info import CaptureInfo
from capture.data_types.uploaded import UploadedContent
import asyncio
from django.test import TestCase

class TestCaptureInfo(TestCase):
    def test_capture_info(self):
        content = """
        Important dates on our return in September
        Tuesday 3 September PUPILS RETURN TO SCHOOL Be Proud Week
        SUFFOLKS CLOSED - INSET DAY - NO TEA-TIME CLUB 
        Wednesday 4 September 
        9.00-10.00 Year 6 parent/carer SATs/Secondary School meeting"""
        expected_output = [
            {'event': "PUPILS RETURN TO SCHOOL Be Proud Week", 'description': "Pupils return to school", 'date_time': '03/09/2024 00:00'},
            {'event': "SUFFOLKS CLOSED - INSET DAY - NO TEA-TIME CLUB", 'description': "Suffolks closed - Inset day - No tea-time club", 'date_time': '03/09/2024 00:00'},
            {'event': "Year 6 parent/carer SATs/Secondary School meeting", 'description': "Year 6 parent/carer SATs/Secondary School meeting", 'date_time': '04/09/2024 09:00'}
            ]
    
        capture_info = CaptureInfo(uploaded_content=UploadedContent(content_id="test_capture_info", content=content))
        asyncio.run(capture_info.execute())
        assert capture_info.executed == True
        # Flexible assertion
        assert len(capture_info.parsed_events) == len(expected_output)
