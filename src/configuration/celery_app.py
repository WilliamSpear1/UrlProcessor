from celery import Celery

from .celery_conf import Config


def make_celery_app() -> Celery:
    # Celery App initialization & configuration.
    celery_app = Celery("url_processor")
    celery_app.config_from_object(Config)
    return celery_app

celery_app = make_celery_app()