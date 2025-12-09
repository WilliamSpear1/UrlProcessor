import logging
import re

logger = logging.getLogger(__name__)

class PageUpdater:
    def __init__(self, url):
        self.url = url

    def update(self, current_page:int):
        updated_url = re.sub(r"p=\d+", f"p={current_page}", self.url)
        logger.info(f"Updated url={updated_url}")
        return updated_url