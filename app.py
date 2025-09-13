import logging
import time

from celery.result import AsyncResult
from flask import request, jsonify, Response, Flask

from tasks import fetch_urls, celery_app

logger = logging.getLogger(__name__)
app = Flask(__name__)

#Configurable retry policy
MAX_RETRIES = 3
RETRY_DELAY = 2 # seconds

# routes for polling task status.
@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id) -> tuple[Response,int]:
    """Endpoint to check the status of a Celery task."""
    task: AsyncResult = celery_app.AsyncResult(task_id)
    logger.info("Checking status for task_id=%s, state=%s", task_id, task.state)

    response = {"state": task.state}
    if task.state == 'PENDING':
        response['status'] = "Pending"
    elif task.state == 'SUCCESS':
        response['status'] = 'Success'
        response['result'] = task.result
    else: # FAILURE, RETRY, STARTED, etc.
        response['status'] = str(task.info) if task.info else "In Progress"

    return jsonify(response), 200

# routes for polling task status.
@app.route('/fetch-urls', methods=['POST'])
def download() -> tuple[Response, int]:
    """Endpoint to start a Celery task for scraping URLs."""
    data = request.get_json()
    url  = data.get('url')

    if not url:
        logger.warning("Missing 'url' in request body")
        return jsonify({'error': 'URL is required'}), 400

    for attempt in range(1, MAX_RETRIES - 1):
        try:
            task = fetch_urls.delay(url)
            logger.info("Submitted task_id=%s for url=%s", task.id, url)
            return jsonify({"task_id": task.id, "status": "processing"}), 202
        except Exception as e:
            logger.error("Error submitting task(attempt %d/%d: %s", attempt, MAX_RETRIES, e)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                return jsonify({"error": str(e)}), 400

    return jsonify({"Error": "Problem occurring with processing URL"}), 500