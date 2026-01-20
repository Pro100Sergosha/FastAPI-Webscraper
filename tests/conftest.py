import asyncio
import os
from typing import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_crawler_service, get_job_store
from app.runner.asgi import app
from app.services.job_store import JobStore


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_storage_path(tmp_path):
    d = tmp_path / "storage"
    d.mkdir()
    return str(d)


@pytest.fixture
def mock_job_store(temp_storage_path):
    return JobStore(storage_path=os.path.join(temp_storage_path, "tasks"))


@pytest.fixture
def mock_crawler_service():
    service = MagicMock()
    service.start = AsyncMock()
    return service


@pytest.fixture
def client(mock_job_store, mock_crawler_service) -> Generator[TestClient, None, None]:

    app.dependency_overrides[get_job_store] = lambda: mock_job_store
    app.dependency_overrides[get_crawler_service] = lambda: mock_crawler_service

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
