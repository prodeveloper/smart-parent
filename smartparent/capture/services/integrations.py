
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from smartparent.config import ConfigLoader
from capture.services.interfaces import LLMModel
import google.generativeai as genai
from capture.services.validators import PostFlightValidator

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


class GeminiModel(LLMModel):
    def __init__(self, gemini_key, gemini_model='gemini-1.5-flash'):
        self.gemini_key = gemini_key
        self.gemini_model = gemini_model
        self.setup()
    def setup(self) -> None:
         genai.configure(api_key=self.gemini_key)
         self.model = genai.GenerativeModel(self.gemini_model)

    def prompt(self, prompt):
        response = self.model.generate_content(prompt)
        candidates = response.candidates[0]
        PostFlightValidator.check_safety_ratings(candidates.safety_ratings)
        return response.text
