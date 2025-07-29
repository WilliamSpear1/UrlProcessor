from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire.webdriver import Chrome
from logs.logger_config import setup_logging

logger = setup_logging(__name__)

class ChromeDriverFactory:
    def __init__(self, url):
        self.url    = url
        self.driver = self.browser()

    def get_driver(self) -> Chrome:
        return self.driver

    def browser(self) -> Chrome:
        options = Options()

        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")


        seleniumwire_options = {
            'verify_ssl': False,
            'mitm_http2': False,
            'connection_timeout': 10,
            'ignore_http_methods': ['CONNECT']
        }

        driver = webdriver.Chrome(seleniumwire_options=seleniumwire_options, options=options)

        # Wait for page and media to load
        (WebDriverWait(driver, 10)
         .until(EC.presence_of_all_elements_located((By.TAG_NAME, "body"))))

        driver.get(self.url)
        return driver

    def change_url(self, new_url) -> None:
        if self.driver:
            self.driver.get(new_url)
            logger.info(f"Changed URL to: {new_url}")
        else:
            logger.info("No browser instance to change URL.")

    def close_browser(self) -> None:
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed successfully.")
        else:
            logger.info("No browser instance to close.")