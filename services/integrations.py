import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
from pdfconverse.models import FilePath, GeminiSetup
from pdfconverse import PDFConverse
from config import ConfigLoader
from google.cloud import storage
from io import BytesIO
import json

class FirebaseIntegration:
    def __init__(self):
        self.db = None

    def setup(self):
        # Check if the app is already initialized. This fails if the app is not initialized. or if you try to initialize it twice. 
        if not firebase_admin._apps:
            cred = credentials.Certificate(ConfigLoader().configs.FIREBASE_SERVICE_ACCOUNT)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    @staticmethod
    def get_db():
        db = FirebaseIntegration()
        if not db.db:
            db.setup()
        return db.db
    def get_collection(self, collection_name: str):
        return self.db.collection(collection_name)
    def get_document(self, collection_name: str, document_id: str):
        return self.db.collection(collection_name).document(document_id)
    
class PdfConverseIntegration:
    """
    This class is used to initialize the PDFConverse services by file path or bytes.
    The only difference in file path is it first checks the file actually exists.
    """
    @staticmethod
    def initialize_services_by_file_path(file_name,gemini_key):
        file_path = FilePath(path=file_name)
        gemini_setup = GeminiSetup(api_key=gemini_key, model="gemini-1.5-flash")
        return PDFConverse(gemini_setup=gemini_setup, file_path=file_path)
    @staticmethod
    def initialize_services_by_bytes(file_bytes,gemini_key):
        gemini_setup = GeminiSetup(api_key=gemini_key, model="gemini-1.5-flash")
        return PDFConverse(gemini_setup=gemini_setup, bytes=file_bytes)
    
class BlobStorageIntegration:
    def __init__(self):
        if ConfigLoader().configs.GOOGLE_APPLICATION_CREDENTIALS:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ConfigLoader().configs.GOOGLE_APPLICATION_CREDENTIALS
        self.storage_client = storage.Client()
    def upload_file_to_blob_storage(self, file_path, bucket_name):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        blob.upload_from_file(file_path)

    def file_stream_from_blob_storage(self, file_path, bucket_name):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        file_stream = BytesIO()
        blob.download_to_file(file_stream)
        return file_stream
