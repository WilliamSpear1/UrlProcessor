from celery import Celery

from UrlProcessor.URLProcessor.chrome_driver_factory import ChromeDriverFactory
from UrlProcessor.URLProcessor.downloader import Downloader

celery_app = Celery("tasks", broker='amqp://guest:qmdB1BZK^vd@192.168.50.182:5672//', backend="redis://192.168.50.182:6379/0")
@celery_app.task(name="tasks.fetch_urls")
def fetch_urls(url) -> dict:
    try:
        chrome_browser  = ChromeDriverFactory(url)
        downloader      = Downloader()

        # Start the browser and scrape multiple videos.
        download_videos = downloader.scarp_multiple_videos(chrome_browser)

        # End Browser session.
        chrome_browser.close_browser()
        return download_videos
    except Exception as e:
        return {'error': str(e)}