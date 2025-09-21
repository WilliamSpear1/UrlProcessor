import logging
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire.webdriver import Chrome

from chrome_driver_factory import ChromeDriverFactory
from title_formatter import TitleFormatter

logger = logging.getLogger(__name__)

class Downloader:
    def scarp_multiple_videos(self, chrome_browser:ChromeDriverFactory) -> dict:
        driver = chrome_browser.get_driver()

        """Scrape multiple video download URLs from page."""
        logger.info("Starting Scraping of videos.")
        video_list = driver.find_elements(By.CSS_SELECTOR, "article.item > div.item-info")
        logger.info("Scraping complete. Found %d videos thumbnails.", len(video_list))
        return self._extract_video_links(video_list)

    def scarp_individual_videos(self, urls:list) -> dict:
        """Scrape multiple video download URLs from file."""
        videos = {}
        title_formatter = TitleFormatter()

        for url in urls:
            href = url
            title = title_formatter.format_title(url)
            if href and title:
                videos[title] = href
        return self._handle_multiple_tabs(videos)

    def _extract_video_links(self, video_titles:list) -> dict[str, str]:
        """Extract titles and hrefs from video elements."""
        videos = {}

        for element in video_titles:
            anchor_element = element.find_element(By.CSS_SELECTOR, 'a')
            href                    = anchor_element.get_attribute('href')
            title                    = anchor_element.get_attribute('title')
            if href and title:
                videos[title] = href

        logger.info(" Extracted Videos %s" , videos)

        return self._handle_multiple_tabs(videos)

    def _handle_multiple_tabs(self, videos:dict) -> dict[str,str] | None:
        """Open each video in a new tab, extract download link, then close tab."""
        download_links = {}

        logger.info("Starting to open multiple tabs with links.")

        for title, href in videos.items():
            logger.info("For Title: %s", title)
            logger.info("For Link: %s", href)

            download_links[title] = self.handle_switch(href)

        logger.info("Download Links: %s", download_links)
        return download_links

    def handle_switch(self, href: str) -> str | None:
        logger.info("Switching to new window.")

        chrome = ChromeDriverFactory(href)
        driver = chrome.get_driver()

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
            )

            time.sleep(5)

            download_link = self._grab_download_link(driver)

            logger.info(f"Download Link: {download_link}")
            return download_link
        finally:
            logger.info("Closing Browser")
            # Close the tab and switch back
            chrome.close_browser()

    def _grab_download_link(self, driver: Chrome) -> str | None:
        DOMAIN_NAME = os.environ.get('DOMAIN')

        logger.info(f"Inspecting network requests for domain {DOMAIN_NAME}")

        for request in driver.requests:
            if request.response:
                if DOMAIN_NAME in request.url:
                    ctype = request.response.headers.get("Content-Type", "")
                    logger.debug(f"Captured: {request.url} (Content-Type: {ctype})")
                    # Only keep likely video/media requests
                    if request.url.endswith("_TPL_.mp4"):
                        return request.url

        logger.error("No Downloadable link has been found")
        return None
