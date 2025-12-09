# python
import re
import page_updater
from page_updater import PageUpdater


class DummyLogger:
    def __init__(self):
        self.messages = []

    def info(self, msg):
        self.messages.append(msg)


def test_update_replaces_page_and_logs():
    page_updater.re = re
    logger = DummyLogger()
    page_updater.logger = logger

    updater = PageUpdater("http://example.com/list?p=1&x=2")
    result = updater.update(5)

    assert result == "http://example.com/list?p=5&x=2"
    assert logger.messages[-1] == f"Updated url={result}"


def test_update_no_param_keeps_url_and_logs():
    page_updater.re = re
    logger = DummyLogger()
    page_updater.logger = logger

    updater = PageUpdater("http://example.com/list?x=2")
    result = updater.update(3)

    assert result == "http://example.com/list?x=2"
    assert logger.messages[-1] == f"Updated url={result}"