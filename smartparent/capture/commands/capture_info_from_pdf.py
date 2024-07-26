from capture.commands.capture_info import CaptureInfo
from capture.data_types.uploaded import UploadedContent
from pypdf import PdfReader
from hashlib import md5
import os


class CaptureInfoFromPdf:
    captured_info: CaptureInfo = None
    executed: bool = False
    file_path: str = None
    pdf_text: str = None
    executed: bool = False
    cache_key: str = None
    parsed_events: list = None

    def __init__(self,*,file_path: str):
        self.file_path = file_path
        self._validate_file_path()

    async def execute(self):
        self._pull_all_text_from_pdf()
        self._validate_below_max_size()
        self._generate_key()
        await self._extract_info()
        self.executed = True
    
    def _pull_all_text_from_pdf(self):
        reader = PdfReader(self.file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        self.pdf_text = text
    
    def _validate_below_max_size(self):
        if len(self.pdf_text) > 100000:
            raise ValueError("PDF text is too large to process.")
    
    def _generate_key(self):
        self.cache_key = md5(self.pdf_text.encode()).hexdigest()

    async def _extract_info(self):
        uploaded_content = UploadedContent(content=self.pdf_text, content_id=self.cache_key)
        self.captured_info = CaptureInfo(uploaded_content=uploaded_content)
        await self.captured_info.execute()
        self.parsed_events = self.captured_info.parsed_events

    def _validate_file_path(self):
        if not os.path.exists(self.file_path):
            raise ValueError("File path does not exist.")

    def __getattr__(self, name):
        if not self.executed and name != "executed":
            raise RuntimeError("Command has not run. Try running the command first.")
        return self.__dict__.get(name)