import pytest
from app.core.config import settings


def test_trigger_scraper(client):
    payload = {"url": "https://example.com"}
    response = client.post("/api/v1/scraper/trigger", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "queued"


def test_get_status_404(client):
    response = client.get("/api/v1/scraper/status/unknown-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_status_success(client, mock_job_store):
    task_id = "test-task-id"
    await mock_job_store.create_job(
        task_id, {"task_id": task_id, "url": "x", "status": "running"}
    )

    response = client.get(f"/api/v1/scraper/status/{task_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_get_logs(client, tmp_path):
    log_file = tmp_path / "scraper.log"
    settings.LOG_FILE = str(log_file)

    response = client.get("/api/v1/scraper/logs")
    assert response.status_code == 200
    assert "Log file not found yet." in response.json()["logs"]

    log_file.write_text("Log line 1\nLog line 2", encoding="utf-8")
    response = client.get("/api/v1/scraper/logs")
    assert response.status_code == 200
    logs = response.json()["logs"]
    assert len(logs) == 2
    assert "Log line 2" in logs
