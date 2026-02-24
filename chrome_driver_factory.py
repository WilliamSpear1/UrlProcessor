from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from seleniumwire.webdriver import Chrome

from conf.logger_conf import setup_logging

logger = setup_logging(__name__)

class ChromeDriverFactory:
    def __init__(self):
        self.driver = self.browser()

    def browser(self) -> Chrome:
        options = Options()

        options.add_argument("--headless=new")  # modern headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  # prevent /dev/shm size issues
        options.add_argument("--disable-gpu")
        options.page_load_strategy = 'eager'

        seleniumwire_options = {
            'verify_ssl': False,
            'mitm_http2': False,
            'connection_timeout': 10,
            'ignore_http_methods': ['CONNECT']
        }

        driver = webdriver.Chrome(seleniumwire_options=seleniumwire_options, options=options)

        logger.debug("Driver initialized and being returned.")

        return driver

    def get_driver(self) -> Chrome:
        return self.driver

    def set_driver(self, new_url) -> None:
        if not self.driver:
            raise Exception("Driver instance is not available to change URL.")
            return None
        elif new_url is None:
            raise Exception("New URL cannot be None.")
            return None

        try:
            self.driver.get(new_url)
            (WebDriverWait(self.driver, 10)
             .until(EC.presence_of_all_elements_located((By.TAG_NAME, "body"))))
            logger.info(f"Changed URL to: {new_url}")
        except Exception as e:
            logger.exception("Failed to charge URL to %s: %s", new_url, e)
            self.driver = None

    def get_url(self) -> str|None:
        if self.driver:
            return self.driver.current_url
        else:
            logger.warning("Driver instance is not available to get URL.")
            return None

    def close_browser(self) -> None:
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed successfully.")
        else:
            logger.info("No browser instance to close.")