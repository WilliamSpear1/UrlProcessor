import re

from conf.logger_conf import setup_logging

logger = setup_logging(__name__)

class PageUpdater:
    def __init__(self, url):
        self.url = url

    def update(self, current_counter:int) -> str:
        current_page = current_counter + 1
        updated_url = re.sub(r"p=\d+", f"p={current_page}", self.url)
        logger.info(f"Updated url={updated_url}")
        return updated_url