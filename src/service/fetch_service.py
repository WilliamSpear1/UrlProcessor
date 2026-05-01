from .downloader_service import DownloaderService
from .page_updater_service import PageUpdaterService
from ..configuration.celery_app import celery_app
from ..configuration.logger_conf import setup_logging
from ..model.chrome_driver import ChromeDriver

logger = setup_logging(__name__)
# Celery App Task.
@celery_app.task(name="tasks.fetch_urls")
def fetch_urls(url:str, number_of_pages:int) -> dict:
    """
    Celery Task: Launch a Chrome browser, scarp downloadable video URLS, and return them.
    """
    chrome_browser = ChromeDriver()
    logger.debug("Launching Chrome Browser")
    try:
        logger.debug("Inside fetch_urls with URL: %s and number_of_pages: %d", url, number_of_pages)
        downloader = DownloaderService()
        page_updater = PageUpdaterService(url)

        download_videos = {}

        for i in range(0, number_of_pages):
            logger.debug("Starting to process url")
            new_url = page_updater.update(i)
            chrome_browser.set_driver(new_url)
            logger.debug("Changed URL to: %s", chrome_browser.get_url())

            logger.info("Start the browser and start scarping videos for URL: %s", chrome_browser.get_url())
            # Start the browser and scrape multiple videos.
            page_results = downloader.scarp_multiple_videos(chrome_browser)
            download_videos.update(page_results)

        logger.info("Scraping complete. Found %d videos.", len(download_videos))
        return download_videos
    except Exception as e:
        logger.exception("Error while fetching URLs for %s", url)
        return {'error': str(e)}
    finally:
        if chrome_browser:
            try:
                # End Browser session.
                chrome_browser.close_browser()
                logger.info("Browser session closed successfully")
            except Exception as close_error:
                logger.warning("Error while closing browser: %s", close_error)