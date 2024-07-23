#I want to print python version
import sys

from models.local_firebase import FirebaseCache
from services.integrations import FirebaseIntegration, PdfConverseIntegration
import configparser
import os
from config import ConfigLoader





def test_cloud_storage():
    db = FirebaseIntegration.get_db()
    doc_ref = db.collection("users").document("alovelace")
    doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})
    users_ref = db.collection("users")
    #I want to assert that the document was created
    assert users_ref.document("alovelace").get().exists
    #delete the record
    doc_ref.delete()
    #I want to assert that the document was deleted
    assert not users_ref.document("alovelace").get().exists

def test_firebase_integration():
    db = FirebaseIntegration.get_db()
    assert db is not None       

def test_cache():
    cache = FirebaseCache()
    cache.set("test", "test")
    assert cache.get("test") == "test"

def test_cache_invalid_key():
    cache = FirebaseCache()
    assert cache.get("invalid_key") is None

def test_keys_loaded():
    assert ConfigLoader().configs.GEMINI_API_KEY is not None
    assert ConfigLoader().configs.FIREBASE_SERVICE_ACCOUNT is not None
    assert ConfigLoader().configs.LOCAL_PASSWORD is not None
    assert ConfigLoader().configs.GOOGLE_APPLICATION_CREDENTIALS is not None



