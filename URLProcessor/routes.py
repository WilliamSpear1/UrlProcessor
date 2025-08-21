import time

from celery.exceptions import NotRegistered
from flask import Blueprint, request, jsonify, Response, json

from URLProcessor.tasks import celery_app, fetch_urls
from logs.logger_config import setup_logging

logger = setup_logging(__name__)
bp = Blueprint('main', __name__)

# routes for polling task status.
@bp.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id) -> tuple[Response,int]:
        task = celery_app.AsyncResult(task_id)

        if task.state == 'PENDING':
                response = {
                        'state': task.state,
                        'status': 'Pending...'
                }
        elif task.state == 'SUCCESS':
                response = {
                        'state': task.state,
                        'result': task.result
                }
        else:
                response = {
                        'state': task.state,
                        'status': str(task.info)  # this is the exception raised
                }
        return jsonify(response), 200

# routes for polling task status.
@bp.route('/fetch-urls', methods=['POST'])
def download() -> tuple[Response, int]:
        MAX_RETRIES = 3
        RETRY_DELAY = 2

        # Retrieve Url from json request.
        data = request.get_json()
        url  = data.get('url')

        if not url:
                return jsonify({'error': 'URL is required'}), 400

        for i in range(MAX_RETRIES):
                try:
                        task = fetch_urls.delay(url)
                        return jsonify({"task_id": task.id, "status": "processing"}), 202
                except NotRegistered as e:
                        if i < MAX_RETRIES - 1:
                                time.sleep(RETRY_DELAY)
                        else:
                                return jsonify({'error': e}), 400
        return jsonify({'Error': 'Problem occurring with processing URL'}), 500

