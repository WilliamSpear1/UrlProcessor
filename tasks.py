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
    try:
        chrome_browser  = ChromeDriverFactory(url)
        downloader          = Downloader()

        logger.info("Start the browser and start scarping videos.")
        # Start the browser and scrape multiple videos.
        download_videos = downloader.scarp_multiple_videos(chrome_browser)

        logger.info("Close the browser task for scraping is finished.")
        # End Browser session.
        chrome_browser.close_browser()
        logger.info(f"Return downloadable videos: {download_videos}")
        return download_videos
    except Exception as e:
        return {'error': str(e)}