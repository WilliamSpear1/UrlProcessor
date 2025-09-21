import logging
from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from chrome_driver_factory import ChromeDriverFactory

logger = logging.getLogger(__name__)
class TitleFormatter:
    def format_title(self, url:str) -> str:
        parts = urlparse(url).path.rstrip("/").split("/")
        title = parts[-1] if parts else None
        names = self._get_names(url)

        all_names = "[" + ",".join(names) + "]"
        result = all_names + title
        return result

    def _get_names(self, href: str) -> list[str]:
        logger.info("Switching to new window.")

        chrome = ChromeDriverFactory(href)
        driver = chrome.get_driver()

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
        )

        h3_elements = driver.find_elements(By.CSS_SELECTOR, '.video-info > div > article .block-details > div h3')

        element = None
        for h3_element in h3_elements:
            text = h3_element.text
            if "Porn-stars" in text:
                logger.info(f"Text: {text}")
                element = h3_element

        a_elements = element.find_elements(By.TAG_NAME, "a")

        name_elements = []

        if a_elements:
            name_elements = [a.text for a in a_elements]

        return name_elements