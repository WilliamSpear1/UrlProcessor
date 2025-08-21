from celery import Celery

from URLProcessor.chrome_driver_factory import ChromeDriverFactory
from URLProcessor.downloader import Downloader
from logs.logger_config import setup_logging

celery_app = Celery("tasks", broker='amqp://guest:qmdB1BZK^vd@192.168.50.182:5672//', backend="redis://192.168.50.182:6379/0")
logger = setup_logging(__name__)

@celery_app.task(name="tasks.fetch_urls")
def fetch_urls(url) -> dict:
    try:
        chrome_browser  = ChromeDriverFactory(url)
        downloader      = Downloader()
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