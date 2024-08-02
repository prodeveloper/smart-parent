from capture.services.local_firebase import FirebaseCache
from capture.services.integrations import FirebaseIntegration
from smartparent.config import ConfigLoader
from django.test import TestCase


class TestCloudStorage(TestCase):
    def test_cloud_storage(self):
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

    def test_firebase_integration(self):
        db = FirebaseIntegration.get_db()
        assert db is not None       

    def test_cache(self):
        cache = FirebaseCache()
        cache.set("test", "test")
        assert cache.get("test") == "test"

    def test_cache_invalid_key(self):
        cache = FirebaseCache()
        assert cache.get("invalid_key") is None

    def test_keys_loaded(self):
        assert ConfigLoader().configs.GEMINI_API_KEY is not None
        assert ConfigLoader().configs.FIREBASE_SERVICE_ACCOUNT is not None
        assert ConfigLoader().configs.LOCAL_PASSWORD is not None
        assert ConfigLoader().configs.GOOGLE_APPLICATION_CREDENTIALS is not None



