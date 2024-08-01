from capture.services.integrations import GeminiModel
from capture.services.validators import PostFlightValidator
from capture.services.integrations import FirebaseIntegration
from smartparent.config import ConfigLoader
from django.test import TestCase


class SafetyRating:
    def __init__(self, category, probability):
        self.category = category
        self.probability = probability

class Candidate:
    def __init__(self, text, role, finish_reason, index, safety_ratings):
        self.text = text
        self.role = role
        self.finish_reason = finish_reason
        self.index = index
        self.safety_ratings = safety_ratings

class TestGemini(TestCase):
    """Test the GeminiModel class"""
    def test_gemini_prompt(self):
        """Test the prompt to gemini returns what is expected"""
        gemini_key = ConfigLoader().configs.GEMINI_API_KEY
        if ConfigLoader().test_config.GEMINI_TEST == "False":
            #We check if we are actually going to run the token consuming test"
            assert True
            return
        model = GeminiModel(gemini_key)
        output = model.prompt(
            """This is part of a unit test, 
            reply using smallest amount of token and ensure you say 'Yes I am live'
            """
            )
        assert 'Yes I am live' in output
    def test_safety_ratings(self):
        """Test the safety ratings"""
        candidates = [
            Candidate(
                text="Yes, I am live \n",
                role="model",
                finish_reason="STOP",
                index=0,
                safety_ratings=[
                    SafetyRating("HARM_CATEGORY_SEXUALLY_EXPLICIT", "NEGLIGIBLE"),
                    SafetyRating("HARM_CATEGORY_HATE_SPEECH", "NEGLIGIBLE"),
                    SafetyRating("HARM_CATEGORY_HARASSMENT", "NEGLIGIBLE"),
                    SafetyRating("HARM_CATEGORY_DANGEROUS_CONTENT", "NEGLIGIBLE")
                ]
            )
        ]
        PostFlightValidator.check_safety_ratings(candidates[0].safety_ratings)