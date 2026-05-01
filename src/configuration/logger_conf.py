#Ensure the logs directory exists
import json
import logging
import logging.config
import os

def safe_load_config() -> logging.Logger | None:
    environment = os.environ.get("ENVIRONMENT")

    try:
        config_file = f'/app/src/configuration/logging_config_{environment}.json'
        with open(config_file, 'r') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        return logging.getLogger()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.basicConfig(level=logging.DEBUG)
        logging.warning("Config file not found, using basicConfig with DEBUG level.")
        return logging.getLogger()


def setup_logging(name) -> logging.Logger:
    """
    Set up logging configuration.
    """
    logger = safe_load_config()
    logger.info(f"Logging is set up in: {name}")

    return logger