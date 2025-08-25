import configparser

class Properties:
    def __init__(self, filename="config.properties"):
        self.config = self.get_config(filename)

    @staticmethod
    def get_config(filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    def get_website_name(self):
        return self.config.get('WebsiteSection', 'website.name')