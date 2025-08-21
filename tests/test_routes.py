from unittest.mock import patch, MagicMock

import pytest

from URLProcessor.wsgi import create_app

@pytest.fixture
def client():
    """Flask Test Client"""
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_task_status_pending(client):
    """Should return pending state response"""
    with patch('URLProcessor.routes.celery_app.AsyncResult') as mock_async:
        mock_async.return_value.state = 'PENDING'
        mock_async.return_value.result = None

        resp = client.get('/task-status/fake_id')
        data = resp.get_json()

        assert resp.status_code == 200
        assert data['state'] == 'PENDING'
        assert  data["status"] == "Pending..."

def test_task_status_success(client):
    """Should return success with result."""
    with patch('URLProcessor.routes.celery_app.AsyncResult') as mock_async:
        mock_async.return_value.state = 'SUCCESS'
        mock_async.return_value.result = {'foo': 'bar'}

        resp = client.get('/task-status/fake_id')
        data = resp.get_json()

        assert resp.status_code == 200
        assert data['state'] == 'SUCCESS'
        assert  data["result"] == {'foo':'bar'}

def test_task_status_failure(client):
    with patch('URLProcessor.routes.celery_app.AsyncResult') as mock_async:
        mock_async.return_value.state = 'FAILURE'
        mock_async.return_value.info = Exception('some error')

        resp = client.get('/task-status/fake_id')
        data = resp.get_json()

        assert resp.status_code == 200
        assert data['state'] == 'FAILURE'
        assert "some error" in data['status']

def test_download_missing_url(client):
    """Should fail if url is missing."""
    resp = client.post('/fetch-urls', json={})
    data = resp.get_json()

    assert resp.status_code == 400
    assert 'error' in data

def test_download_success(client):
    """Should start task and return 202."""
    mock_task = MagicMock()
    mock_task.id = "12345"

    with patch('URLProcessor.routes.fetch_urls') as mock_fetch:
        mock_fetch.delay.return_value = mock_task

        resp = client.post('/fetch-urls', json={'url': 'http://example.com'})
        data = resp.get_json()

        assert resp.status_code == 202
        assert data['task_id'] == '12345'
        assert data['status'] == "processing"

def test_download_not_registered(client):
    """Should retry and fail with 400 if Not Registered persists."""
    with patch('URLProcessor.routes.fetch_urls.delay', side_effect=Exception('Task Not Registered')):
        resp = client.post('/fetch-urls', json={'url': 'http://example.com'})
        data = resp.get_json()

        assert data["error"]  == "Task Not Registered"
        assert resp.status_code == 400