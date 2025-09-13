import logging
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from chrome_driver_factory import ChromeDriverFactory

logger = logging.getLogger(__name__)

class Downloader:
    def __init__(self, chrome_browser:ChromeDriverFactory):
        self._chrome_browser = chrome_browser

    def scarp_multiple_videos(self) -> dict:
        driver = self._chrome_browser.get_driver()

        """Scrape multiple video download URLs from page."""
        logger.info("Starting Scraping of videos.")
        video_list = driver.find_elements(By.CSS_SELECTOR, "article.item > div.item-info")
        logger.info("Scraping complete. Found %d videos thumbnails.", len(video_list))
        return self._extract_video_links(video_list)

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
        driver = self._chrome_browser.get_driver()

        """Open each video in a new tab, extract download link, then close tab."""
        download_links = {}
        main_window = driver.current_window_handle

        logger.info("Starting to open multiple tabs with links.")

        for title, href in videos.items():
            logger.info("Title: %s", title)
            logger.info("Link: %s", href)

            try:
                driver.execute_script("window.open(arguments[0]);", href)
                new_window = driver.window_handles[-1]
                driver.switch_to.window(new_window)

                (WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
                )

                download_link = self._grab_download_link(href)

                if download_link:
                    download_links[title] = download_link

                logger.info("Processing video: %s", href)
            except Exception as e:
                logger.info('Error Processing %s: %s', href, e)
            finally:
                driver.close()
                #Ensure main window still exists before switching.
                if main_window in driver.window_handles:
                    driver.switch_to.window(main_window)
                else :
                    logger.error("Main window handle not found after closing tab.")
                    break

        logger.info("Download Links: %s", download_links)
        return download_links

    def _grab_download_link(self, url:str) -> str | None:
        """Inspect network requests to find the downloadable link."""
        logger.info("HERE")
        DOMAIN_NAME = os.environ.get('DOMAIN')
        self._chrome_browser.change_url(url)
        driver = self._chrome_browser.get_driver()

        logger.info(f"Grabbing downloadable link from this url: {url}")
        logger.info(f"Domain: {DOMAIN_NAME}")

        for request in driver.requests:
            if request.response:
                request_url = request.url.lower()
                if DOMAIN_NAME in request_url:
                    logger.info("Found matching URL: %s", request.url)
                    return request.url

        logger.info("No download link found for URL: ", url)
        return None
