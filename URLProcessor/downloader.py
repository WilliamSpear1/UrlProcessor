from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logs.logger_config import setup_logging

logger = setup_logging(__name__)

class Downloader:
    PORN_HITS = "ahcdn.pornhits"

    def scarp_multiple_videos(self, chrome_driver) -> dict:
        driver              = chrome_driver.get_driver()
        video_titles      = driver.find_elements(By.CSS_SELECTOR, "article.item > div.item-info")
        videos              = self.grab_hrefs(video_titles)
        download_urls = self.handle_multiple_tabs(chrome_driver, videos)

        return download_urls

    def grab_hrefs(self, video_titles) -> dict:
        videos = {}

        for element in video_titles:
            anchor_element = element.find_element(By.CSS_SELECTOR, 'a')
            href                    = anchor_element.get_attribute('href')
            title                    = anchor_element.get_attribute('title')
            videos[title]        = href

        return videos

    def handle_multiple_tabs(self, chrome_driver, videos) -> dict:
        download_links = {}
        driver = chrome_driver.get_driver()

        for title, href in videos.items():
            driver.execute_script("window.open(arguments[0]);", href)
            driver.switch_to.window(driver.window_handles[-1])

            (WebDriverWait(driver, 10)
             .until(EC.presence_of_all_elements_located((By.TAG_NAME, "body"))))

            download_links[title] = self.grab_download_link(chrome_driver, href)
            logger.info(f"Processing video: {href}")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        return download_links

    def grab_download_link(self, chrome_driver, url) -> str | None:
        chrome_driver.change_url(url)
        driver = chrome_driver.get_driver()

        for request in driver.requests:
            if request.response:
                url = request.url.lower()
                if self.PORN_HITS in url:
                    logger.info("Needed URL: ", request.url)
                    return request.url

        logger.info("No download link found for URL: ", url)
        return None
