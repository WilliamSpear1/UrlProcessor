from configparser import ConfigParser
from logs.logger_config import setup_logging

logger = setup_logging(__name__)

class Properties:
    def __init__(self):
        self.config = self.get_config()

    def get_config(self):
        config = ConfigParser.RawConfigParser()
        config.read('config.properties')
        return config.read('config.properties')

    def get_website_name(self):
        return self.config.get('WebsiteSection', 'website.name')