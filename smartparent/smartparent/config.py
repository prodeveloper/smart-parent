import configparser
import os
from collections import namedtuple
import json

class ConfigLoader:
    """Loads and manages configuration settings for the application."""
    database_config = namedtuple('DatabaseConfig', [
            'PUBLIC_IP_ADDRESS', 'DATABASE_NAME', 'USER', 'PASSWORD'
        ])
    gemini_config = namedtuple('Config', [
            'GEMINI_API_KEY', 'FIREBASE_SERVICE_ACCOUNT', 'LOCAL_PASSWORD', 'GOOGLE_APPLICATION_CREDENTIALS'
        ])

    def __init__(self):
        self._db_configs()

    @property
    def configs(self):
        """Retrieve Gemini configuration, prioritizing environment variables."""
        config = configparser.ConfigParser()
        config.read('../config.ini')
        # Prioritize environment variables set in Cloud Run
        self.gemini_config.GEMINI_API_KEY = (
            os.environ.get('gemini') or
            config.get('GEMINI', 'GEMINI_API_KEY', fallback=None)
        )
        self.gemini_config.LOCAL_PASSWORD = (
            os.environ.get('password') or
            config.get('LOCAL', 'PASSWORD', fallback=None)
        )
        #Because Firebase expects a dictionary while Google application credentials expects a string
        if os.environ.get('firebase'):
            self.gemini_config.FIREBASE_SERVICE_ACCOUNT = json.loads(os.environ.get('firebase'))
            self.gemini_config.GOOGLE_APPLICATION_CREDENTIALS = None
        else:
            self.gemini_config.FIREBASE_SERVICE_ACCOUNT = (
                os.environ.get('firebase') or
                config.get('GEMINI', 'FIREBASE_SERVICE_ACCOUNT', fallback=None)
            )
            self.gemini_config.GOOGLE_APPLICATION_CREDENTIALS = self.gemini_config.FIREBASE_SERVICE_ACCOUNT


        return self.gemini_config
    def _db_configs(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        self.database_config = namedtuple('DatabaseConfig', [
            'PUBLIC_IP_ADDRESS', 'DATABASE_NAME', 'USER', 'PASSWORD'
        ])
        self.database_config.PUBLIC_IP_ADDRESS = (
            os.environ.get('PUBLIC_IP_ADDRESS') or
            config.get('DATABASE', 'PUBLIC_IP_ADDRESS', fallback=None)
        )
        self.database_config.DATABASE_NAME = (
            os.environ.get('DATABASE_NAME') or
            config.get('DATABASE', 'DATABASE_NAME', fallback=None)
        )
        self.database_config.USER = (
            os.environ.get('USER') or
            config.get('DATABASE', 'USER', fallback=None)
        )
        self.database_config.PASSWORD = (
            os.environ.get('PASSWORD') or
            config.get('DATABASE', 'PASSWORD', fallback=None)
        )

    def max_text_length(self):
        default_max_text_length = 10000
        max_text_length = (
            os.environ.get('max_text_length') or
            default_max_text_length
        )
        return max_text_length
    def max_times_run_today(self):
        default_max_times_run_today = 20
        max_times_run_today = (
            os.environ.get('max_times_run_today') or
            default_max_times_run_today
        )
        return max_times_run_today