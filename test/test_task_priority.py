import pytest
import requests
from .conftest import ENDPOINT_TASKS, ENDPOINT_TASK_BY_ID


class TestTaskPriorityValidation:
    """Tests for task priority validation"""

    @pytest.mark.parametrize("priority", ["LOW", "MIDDLE", "HIGH"])
    def test_create_task_valid_priorities(self, base_url, valid_task_data, priority):
        """Test creating tasks with all valid priority values"""
        task_data = valid_task_data.copy()
        task_data["priority"] = priority

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["priority"] == priority

    @pytest.mark.parametrize("priority", ["LOW", "MIDDLE", "HIGH"])
    def test_update_task_valid_priorities(self, base_url, created_task, priority):
        """Test updating task with all valid priority values"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "priority": priority
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["priority"] == priority

    def test_create_task_default_priority(self, base_url, valid_task_data):
        """Test that default priority is MIDDLE when not provided"""
        task_data = valid_task_data.copy()
        if "priority" in task_data:
            del task_data["priority"]

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["priority"] == "MIDDLE"

    @pytest.mark.parametrize("invalid_priority", ["CRITICAL", "URGENT", "low", "high", "", "NONE"])
    def test_create_task_invalid_priority(self, base_url, valid_task_data, invalid_priority):
        """Test creating tasks with invalid priority values"""
        task_data = valid_task_data.copy()
        task_data["priority"] = invalid_priority

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        # Should return 400 for invalid priority
        assert response.status_code == 400

    @pytest.mark.parametrize("invalid_priority", ["CRITICAL", "URGENT", "low", "high", ""])
    def test_update_task_invalid_priority(self, base_url, created_task, invalid_priority):
        """Test updating task with invalid priority values"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "priority": invalid_priority
        }

        response = requests.put(base_url + endpoint, json=update_data)

        # Should return 400 for invalid priority
        assert response.status_code == 400

    def test_priority_persists_across_updates(self, base_url, valid_task_data):
        """Test that priority persists when other fields are updated"""
        # Create task with HIGH priority
        task_data = valid_task_data.copy()
        task_data["priority"] = "HIGH"
        create_response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)
        assert create_response.status_code == 201
        task = create_response.json()
        assert task["priority"] == "HIGH"

        # Update title only
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=task["id"])
        update_data = {"title": "Updated Title"}
        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 200
        updated_task = update_response.json()

        # Priority should remain HIGH
        assert updated_task["priority"] == "HIGH"
        assert updated_task["title"] == "Updated Title"