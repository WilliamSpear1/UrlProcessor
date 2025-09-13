import os


class Properties:
    @staticmethod
    def get_domain_name():
        return os.environ.get('DOMAIN')