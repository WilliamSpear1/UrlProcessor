from celery import Celery

from .celery_conf import Config


def make_celery_app(config: Config) -> Celery:
    # Celery App initialization & configuration.
    celery_app = Celery("url_processor")
    celery_app.config_from_object(config)
    return celery_app

celery_app = make_celery_app(Config)