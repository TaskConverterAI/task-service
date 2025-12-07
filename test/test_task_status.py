import pytest
import requests
from .conftest import ENDPOINT_TASKS, ENDPOINT_TASK_BY_ID


class TestTaskStatusValidation:
    """Tests for task status validation"""

    @pytest.mark.parametrize("status", ["DONE", "UNDONE"])
    def test_update_task_valid_status(self, base_url, created_task, status):
        """Test updating task with all valid status values"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "status": status
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["status"] == status

    def test_task_initial_status(self, base_url, valid_task_data):
        """Test that newly created task has a default status"""
        response = requests.post(base_url + ENDPOINT_TASKS, json=valid_task_data)

        assert response.status_code == 201
        task = response.json()
        assert "status" in task
        assert task["status"] in ["DONE", "UNDONE"]

    def test_task_default_status_is_undone(self, base_url, valid_task_data):
        """Test that newly created task defaults to UNDONE status"""
        response = requests.post(base_url + ENDPOINT_TASKS, json=valid_task_data)

        assert response.status_code == 201
        task = response.json()
        # Most task management systems default to incomplete/undone
        assert task["status"] == "UNDONE"

    @pytest.mark.parametrize("invalid_status", ["COMPLETED", "INCOMPLETE", "PENDING", "done", "undone", ""])
    def test_update_task_invalid_status(self, base_url, created_task, invalid_status):
        """Test updating task with invalid status values"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "status": invalid_status
        }

        response = requests.put(base_url + endpoint, json=update_data)

        # Should return 400 for invalid status
        assert response.status_code == 400

    def test_status_transition_undone_to_done(self, base_url, valid_task_data):
        """Test transitioning task status from UNDONE to DONE"""
        # Create task (should be UNDONE by default)
        create_response = requests.post(base_url + ENDPOINT_TASKS, json=valid_task_data)
        assert create_response.status_code == 201
        task = create_response.json()
        initial_status = task["status"]

        # Update to DONE
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=task["id"])
        update_data = {"status": "DONE"}
        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 200
        updated_task = update_response.json()

        assert updated_task["status"] == "DONE"
        assert initial_status == "UNDONE"

    def test_status_transition_done_to_undone(self, base_url, valid_task_data):
        """Test transitioning task status from DONE back to UNDONE"""
        # Create task
        create_response = requests.post(base_url + ENDPOINT_TASKS, json=valid_task_data)
        assert create_response.status_code == 201
        task = create_response.json()

        # Set to DONE
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=task["id"])
        update_data = {"status": "DONE"}
        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 200

        # Set back to UNDONE
        update_data = {"status": "UNDONE"}
        final_response = requests.put(base_url + endpoint, json=update_data)
        assert final_response.status_code == 200
        final_task = final_response.json()

        assert final_task["status"] == "UNDONE"

    def test_status_persists_across_updates(self, base_url, valid_task_data):
        """Test that status persists when other fields are updated"""
        # Create task
        create_response = requests.post(base_url + ENDPOINT_TASKS, json=valid_task_data)
        assert create_response.status_code == 201
        task = create_response.json()

        # Set status to DONE
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=task["id"])
        update_data = {"status": "DONE"}
        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 200

        # Update title only
        update_data = {"title": "New Title"}
        final_response = requests.put(base_url + endpoint, json=update_data)
        assert final_response.status_code == 200
        final_task = final_response.json()

        # Status should remain DONE
        assert final_task["status"] == "DONE"
        assert final_task["title"] == "New Title"

    def test_status_and_priority_update_together(self, base_url, created_task):
        """Test updating both status and priority simultaneously"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "status": "DONE",
            "priority": "LOW"
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["status"] == "DONE"
        assert updated_task["priority"] == "LOW"