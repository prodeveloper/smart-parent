import json
import re
from datetime import datetime
from hashlib import md5
from capture.data_types.uploaded import UploadedContent
from capture.models.local_firebase import FirebaseCache
from capture.services.integrations import GeminiModel
from smartparent.config import ConfigLoader
from capture.commands.log_item import LogItem



class CaptureInfo:
    """
    Takes in different types of information and returns proposed dates
    """
    uploaded_content: UploadedContent
    prompt: str
    parsed_events: list[dict]
    executed: bool = False
    def __init__(self, *, uploaded_content: UploadedContent):
        self.uploaded_content = uploaded_content
        self.prompt = self._get_prompt()

    async def execute(self):
        self._gen_content_id()
        await self._parse_events()
        self.executed = True
        LogItem(f"Parsed events: {self.parsed_events}").log()
    
    def _gen_content_id(self):
        full_content = self.prompt+self.uploaded_content.content
        self.uploaded_content.content_id = md5(full_content.encode('utf-8')).hexdigest()
    
    async def _parse_events(self):
        parsed = FirebaseCache().get(self.uploaded_content.content_id)
        if parsed is None:
            parsed = await self._gemini_parse_events()
            LogItem(f"No events found for {self.uploaded_content.content_id} using Gemini").log()
            FirebaseCache().set(self.uploaded_content.content_id, parsed)
        try:
            self.parsed_events = self._clean_parsed_events(parsed)
            LogItem(self.parsed_events).log()
        except json.JSONDecodeError as exc:
            LogItem(f"Failed to parse events: {parsed}").log()
            raise ValueError("Failed to parse events") from exc
        
    def _clean_parsed_events(self, parsed):
        data = re.sub(r"'", r'"', parsed)
        return json.loads(data)
    async def _gemini_parse_events(self):
        gemini_key = ConfigLoader().configs.GEMINI_API_KEY
        model = GeminiModel(gemini_key)
        parsed = model.prompt(self.prompt)
        return parsed
        

    def __getattr__(self, name):
        if not self.executed:
            raise RuntimeError("Command has not run. Try running the command first.")
        return self.__dict__.get(name)
    
    def _get_prompt(self):
        default_year = datetime.now().year
        default_month = datetime.now().month
        default_day = datetime.now().day
        default_hour = default_minute = 0
        
        prompt = f"""From the text below please extract the following information event and date. 
        Give response as JSON for example.
    [{{
        'event': 'event name',
        'description': 'event description',
        'date_time': 'date and time'
    }}]
    In case of multiple events, return a list of events and dates. eg
    [
        {{'event': 'event name', 'description': 'event description', 'date_time': 'date and time'}},
        {{'event': 'event name', 'description': 'event description', 'date_time': 'date and time'}}
    ]

    Give a full date. Incase a year is not present use: {default_year}, 
    if month {default_month}
    date {default_day}
    For time use {default_hour:02d}:{default_minute:02d}
    . Date_time should be in the format dd/mm/yyyy hh:mm
    Please include nothing else in your response. If you can't find the information, return an empty list.:
    """
        return prompt + self.uploaded_content.content


