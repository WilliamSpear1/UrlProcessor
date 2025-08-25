import logging
import os
from celery import Celery
from chrome_driver_factory import ChromeDriverFactory
from downloader import Downloader

logger = logging.getLogger(__name__)

# Celery App initialization & configuration.
celery_app = Celery(
    "URLProcessor",
    backend=os.environ['CELERY_RESULT_BACKEND'],
    broker=os.environ['CELERY_BROKER_URL']
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Celery App Task.
@celery_app.task
def fetch_urls(url:str) -> dict:
    """
    Celery Task: Launch a Chrome browser, scarp downloadable video URLS, and return them.
    """
    # TODO: Update to acquire links from multiple pages.
    chrome_browser = None
    try:
        chrome_browser  = ChromeDriverFactory(url)
        downloader          = Downloader(chrome_browser)

        logger.info("Start the browser and start scarping videos for URL: %s", url)

        # Start the browser and scrape multiple videos.
        download_videos = downloader.scarp_multiple_videos()

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