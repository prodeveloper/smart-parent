from data_types.uploaded import UploadedContent
from models.local_firebase import FirebaseCache
from services.integrations import GeminiModel
from config import ConfigLoader
import json
import re
import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('debug.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

class CaptureInfo:
    """
    Takes in different types of information and returns proposed dates
    """
    uploaded_content: UploadedContent
    prompt: str
    parsed_events: list[dict]
    executed: bool = False
    def __init__(self, uploaded_content):
        self.uploaded_content = uploaded_content
        self.prompt = self._get_prompt()

    async def execute(self):
        await self._parse_events()
        self.executed = True
        
    async def _parse_events(self):
        parsed = FirebaseCache().get(self.uploaded_content.content_id)
        if parsed is None:
            parsed = await self._gemini_parse_events()
            FirebaseCache().set(self.uploaded_content.content_id, parsed)
        try:
            self.parsed_events = self._clean_parsed_events(parsed)
            logger.info(self.parsed_events)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse events: {parsed}")
            raise ValueError("Failed to parse events")
        
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
        return """From the text below please extract the following information event and date. 
        Give response as JSON for example.
    [{
        'event': 'event name',
        'date': 'date'
    }]
    In case of multiple events, return a list of events and dates. eg
    [
        {'event': 'event name', 'date': 'date'},
        {'event': 'event name', 'date': 'date'}
    ]
    Please include nothing else in your response. If you can't find the information, return an empty list.:
    """ + self.uploaded_content.content


