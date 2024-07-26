from pydantic import BaseModel

class UploadedContent(BaseModel):
    """
    Takes in different types of information and returns proposed dates
    """
    content_id: str
    content: str