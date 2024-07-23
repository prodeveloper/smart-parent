import configparser
import os
from collections import namedtuple
import json

class ConfigLoader:
    @property
    def configs(self):
        config = configparser.ConfigParser()
        config.read('config.ini') 
        Config = namedtuple('Config', ['GEMINI_API_KEY', 'FIREBASE_SERVICE_ACCOUNT', 'LOCAL_PASSWORD', 'GOOGLE_APPLICATION_CREDENTIALS'])
        # Prioritize environment variables set in Cloud Run
        GEMINI_API_KEY = os.environ.get('gemini') if os.environ.get('gemini') else config.get('GEMINI', 'GEMINI_API_KEY', fallback=None)
        LOCAL_PASSWORD = os.environ.get('password') if os.environ.get('password') else config.get('LOCAL', 'PASSWORD', fallback=None)
        #Because Firebase expects a dictionary while Google application credentials expects a string
        if(os.environ.get('firebase')):
            FIREBASE_SERVICE_ACCOUNT = json.loads(os.environ.get('firebase'))
            GOOGLE_APPLICATION_CREDENTIALS = None
        else:
            FIREBASE_SERVICE_ACCOUNT = config.get('GEMINI', 'FIREBASE_SERVICE_ACCOUNT', fallback=None)
            GOOGLE_APPLICATION_CREDENTIALS = FIREBASE_SERVICE_ACCOUNT


        return Config(GEMINI_API_KEY, FIREBASE_SERVICE_ACCOUNT, LOCAL_PASSWORD, GOOGLE_APPLICATION_CREDENTIALS)
    
    def get_prompt(self):
        default_prompt = "Explain this to me maximum 5 bullet points as simply as possible. Use metaphors and analogies to explain the concepts."
        prompt = os.environ.get('prompt') if os.environ.get('prompt') else default_prompt
        return prompt