import configparser
import os
from collections import namedtuple
import json

class ConfigLoader:
    """Loads and manages configuration settings for the application."""
    database_config = namedtuple('DatabaseConfig', [
            'DB_HOST', 
            'DB_NAME', 
            'DB_USER', 
            'DB_PASSWORD',
            'IS_PRIVATE',
            'INSTANCE_CONNECTION_NAME',
            'DB_PORT'
        ])
    gemini_config = namedtuple('Config', [
            'GEMINI_API_KEY', 
            'FIREBASE_SERVICE_ACCOUNT', 
            'LOCAL_PASSWORD', 
            'GOOGLE_APPLICATION_CREDENTIALS'
        ])
    test_config = namedtuple('TestConfig', [
            'GEMINI_TEST'
        ])
    throttle_config = namedtuple('ThrottleConfig', [
            'MAX_TEXT_LENGTH',
            'MAX_TIMES_PER_DAY'
        ])
    sendgrid_config = namedtuple('SendgridConfig', [
            'SENDGRID_API_KEY',
            'SENDGRID_FROM',
            'SENDGRID_SANDBOX_MODE_IN_DEBUG',
            'SENDGRID_ECHO_TO_STDOUT'
        ])
    django_config = namedtuple('DjangoConfig', [
            'DJANGO_SUPERUSER_USERNAME',
            'DJANGO_SUPERUSER_EMAIL',
            'DJANGO_SUPERUSER_PASSWORD',
            'DJANGO_SECRET',
            'DJANGO_DEBUG'
        ])

    def __init__(self):
        self._db_configs()
        self._test_configs()
        self._throttle_configs()
        self._sendgrid_configs()
        self._django_superuser_configs()
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
        for field in self.database_config._fields:
            setattr(self.database_config, field,
                    os.environ.get(field) or
                    config.get('DATABASE', field, fallback=None))
    def _test_configs(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        for field in self.test_config._fields:
            setattr(self.test_config, field,
                    os.environ.get(field) or
                    config.get('TEST', field, fallback=None))
    def _throttle_configs(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        for field in self.throttle_config._fields:
            setattr(self.throttle_config, field,
                    int(os.environ.get(field) or
                    config.get('THROTTLE', field, fallback=None)))
    def _sendgrid_configs(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        for field in self.sendgrid_config._fields:
            setattr(self.sendgrid_config, field,
                    os.environ.get(field) or
                    config.get('SENDGRID', field, fallback=None))
    def _django_superuser_configs(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        for field in self.django_config._fields:
            setattr(self.django_config, field,
                    os.environ.get(field) or
                    config.get('DJANGO_CONFIG', field, fallback=None))
