from hashlib import md5
from pydantic import BaseModel, validator, ConfigDict
import logging
from models.local_firebase import FirebaseCache
from io import BytesIO
from typing import Annotated
import base64

"""
This is a validator for the BytesIO type.
It will convert the BytesIO to a base64 encoded string if it is not already a string.
"""
def bytesio_validator(v):
    if isinstance(v, BytesIO):
        return v
    if isinstance(v, (str, bytes)):
        return BytesIO(base64.b64decode(v) if isinstance(v, str) else v)
    raise ValueError('Invalid type for BytesIO')
BytesIOAnnotated = Annotated[BytesIO, bytesio_validator]

class UploadedFile(BaseModel):
    name: str
    data: BytesIOAnnotated | bytes
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def model_dump(self, *args, **kwargs):
        d = super().model_dump(*args, **kwargs)
        if isinstance(d['data'], BytesIO):
            d['data'] = base64.b64encode(d['data'].getvalue()).decode('utf-8')
        return d



class KeyDetails(BaseModel):
    page_start: int
    page_end: int
    uploaded_file: UploadedFile


    @validator('page_end')
    def check_page_range(cls, page_end, values):
        if 'page_start' in values and page_end < values['page_start']:
            raise ValueError('page_end must be greater than or equal to page_start')
        return page_end
    

class PresentationService:
    @staticmethod
    def generate_unique_file_name(uploaded_file: UploadedFile):
        return f"{uploaded_file.name}"
    """
    Generates a unique key for the summary
    This is per page basis and will NOT change if you change the prompt
    """
    @staticmethod
    def generate_unique_key(key_details: KeyDetails):
        return f"summary_{key_details.page_start}_{key_details.page_end}_{key_details.uploaded_file.name}"
   
    @staticmethod
    def get_summary(pdfconverse, page_start:int, page_end:int, uploaded_file: UploadedFile,prompt:str):
        key_details = KeyDetails(page_start=page_start, page_end=page_end, uploaded_file=uploaded_file)
        key: str = PresentationService.generate_unique_key(key_details)
        summary = FirebaseCache().get(key)
        if summary is None:
            logging.debug(msg=f"No summary found for {key}, generating new summary")
            summary = pdfconverse.page(page_start=page_start, page_end=page_end).prompt(prompt)
        FirebaseCache().set(key, summary)
        return summary

        