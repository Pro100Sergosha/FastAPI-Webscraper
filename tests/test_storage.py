import os
import pytest
from app.services.storage import FileSystemStorage
from app.services.job_store import JobStore


@pytest.mark.asyncio
async def test_file_system_storage(tmp_path):
    storage_path = str(tmp_path / "html")
    storage = FileSystemStorage(storage_path)

    filename = storage.generate_filename("https://example.com/foo/bar")
    assert filename == "foo_bar.html"

    filename_root = storage.generate_filename("https://example.com/")
    assert filename_root == "index.html"

    await storage.save("test.html", "<html>content</html>")
    assert os.path.exists(os.path.join(storage_path, "test.html"))


@pytest.mark.asyncio
async def test_job_store(tmp_path):
    storage_path = str(tmp_path / "tasks")
    store = JobStore(storage_path)

    task_id = "task-123"
    init_data = {"status": "queued", "url": "http://test.com"}

    await store.create_job(task_id, init_data)

    job = await store.get_job(task_id)
    assert job["status"] == "queued"
    assert job["created_at"] is not None

    await store.update_job(task_id, {"status": "running", "processed": 10})
    job = await store.get_job(task_id)
    assert job["status"] == "running"
    assert job["processed"] == 10

    missing = await store.get_job("missing_id")
    assert missing is None
