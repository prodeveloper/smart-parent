

from commands.capture_info import CaptureInfo
from data_types.uploaded import UploadedContent

def test_capture_info():
    content = """happening our caterers will be offering a range of cold lunches: rolls, sandwiches, wraps and fruit/ice cream. There 
will be a choice of fillings. 
Important dates on our return in September
Tuesday 3 September PUPILS RETURN TO SCHOOL Be Proud Week
SUFFOLKS CLOSED - INSET DAY - NO TEA-TIME CLUB 
Wednesday 4 September 
9.00-10.00 Year 6 parent/carer SATs/Secondary School meeting 
Please see page 2 for details of the Local Authority’s secondary event on
12 September – click to see the flyer on how to book a place
Thursday 5 September Pupil photos """
    expected_output = [
{"event": "PUPILS RETURN TO SCHOOL Be Proud Week", "date": "03/09/2024"},
{"event": "SUFFOLKS CLOSED - INSET DAY - NO TEA-TIME CLUB", "date": "03/09/2024"},
{"event": "Year 6 parent/carer SATs/Secondary School meeting", "date": "04/09/2024"},
{"event": "Pupil photos", "date": "05/09/2024"},
{"event": "Local Authority's secondary event", "date": "12/09/2024"}
]
    
    capture_info = CaptureInfo(UploadedContent(content_id="test", content=content))
    capture_info.execute()
    assert capture_info.executed == True
    #assert capture_info.parsed_events == expected_output
