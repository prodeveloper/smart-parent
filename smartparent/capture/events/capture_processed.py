from smartparent.capture.commands.capture_info import CaptureInfo
from smartparent.capture.models import CaptureEvent


class CaptureProcessedEvent:
    def __init__(self, capture_info: CaptureInfo):
        self.capture_info = capture_info
    
    def broadcast(self):
        pass
    def save_db(self):
        pass
    