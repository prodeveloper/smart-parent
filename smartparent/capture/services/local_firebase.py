from capture.services.interfaces import ICache
from capture.services.integrations import FirebaseIntegration
from pydantic import BaseModel
from typing import Union

class FirebaseCache(ICache):
    """
    A cache implementation that uses Firebase as the backend.
    """
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str):
        validated_key = CacheKey(key=key).key
        db = FirebaseIntegration.get_db()
        doc_ref = db.collection('smartpdf_cache').document(validated_key)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()['value']
        else:
            return None

    def set(self, key, value):
        validated_key = CacheKey(key=key).key
        validated_value = CacheValue(value=value).value
        db = FirebaseIntegration.get_db()
        doc_ref = db.collection('smartpdf_cache').document(validated_key)
        doc_ref.set({'value': validated_value})
        self.cache[key] = value

class CacheKey(BaseModel):
    key: str
class CacheValue(BaseModel):
    value: Union[str,int]