import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

import aiofiles


class JobStore:
    def __init__(self, storage_path: str = "./storage/tasks"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def _get_path(self, task_id: str) -> str:
        return os.path.join(self.storage_path, f"{task_id}.json")

    async def create_job(self, task_id: str, init_data: Dict[str, Any]):
        """Creates task file id with initial data"""
        init_data["created_at"] = datetime.now().isoformat()
        init_data["updated_at"] = datetime.now().isoformat()
        filepath = self._get_path(task_id)
        async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
            await f.write(json.dumps(init_data, indent=2))

    async def update_job(self, task_id: str, updates: Dict[str, Any]):
        """Updates existing task file"""
        current_data = await self.get_job(task_id)
        if not current_data:
            return

        current_data.update(updates)
        current_data["updated_at"] = datetime.now().isoformat()

        filepath = self._get_path(task_id)
        async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
            await f.write(json.dumps(current_data, indent=2))

    async def get_job(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Reads existing task file"""
        filepath = self._get_path(task_id)
        if not os.path.exists(filepath):
            return None

        async with aiofiles.open(filepath, "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
