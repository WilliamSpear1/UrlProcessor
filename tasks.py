import logging
import os

from celery import Celery

from chrome_driver_factory import ChromeDriverFactory
from downloader import Downloader
from logs.logger_config import setup_logging
from page_updater import PageUpdater

logger = setup_logging(__name__)

# Celery App initialization & configuration.
celery_app = Celery(
    "url_processor",
    backend=os.environ['CELERY_RESULT_BACKEND'],
    broker=os.environ['CELERY_BROKER_URL']
)

celery_app.conf.update(
    task_default_queue = "url_processor_queue",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True
)

# Celery App Task.
@celery_app.task
def fetch_urls(url:str, number_of_pages:int) -> dict:
    """
    Celery Task: Launch a Chrome browser, scarp downloadable video URLS, and return them.
    """
    chrome_browser = ChromeDriverFactory()
    logger.debug("Launching Chrome Browser")
    try:
        logger.debug("Inside fetch_urls with URL: %s and number_of_pages: %d", url, number_of_pages)
        downloader = Downloader()
        page_updater = PageUpdater(url)

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

@celery_app.task
def upload_urls(urls: list) -> dict:
    """
    Celery Task: Scarp downloadable video URLS, and return them.
    """
    downloader = Downloader()
    download_videos = downloader.scarp_individual_videos(urls)

    return download_videos