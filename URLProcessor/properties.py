import configparser
from configparser import ConfigParser
from logs.logger_config import setup_logging

logger = setup_logging(__name__)

class Properties:
    def __init__(self, filename="config.properties"):
        self.config = self.get_config(filename)

    def get_config(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    def get_website_name(self):
        return self.config.get('WebsiteSection', 'website.name')