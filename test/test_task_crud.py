import pytest
import requests
from datetime import datetime, timedelta
from .conftest import (
    ENDPOINT_TASKS,
    ENDPOINT_TASK_BY_ID,
    ENDPOINT_PERSONAL_TASKS,
    ENDPOINT_USER_TASKS,
    ENDPOINT_GROUP_TASKS
)


class TestTaskCreation:
    """Tests for creating tasks"""

    def test_create_personal_task_success(self, base_url, valid_task_data):
        """Test successful creation of a personal task"""
        response = requests.post(base_url + ENDPOINT_TASKS, json=valid_task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["title"] == valid_task_data["title"]
        assert task["description"] == valid_task_data["description"]
        assert task["authorId"] == valid_task_data["authorId"]
        assert task["status"] in ["DONE", "UNDONE"]
        assert task["priority"] in ["LOW", "MIDDLE", "HIGH"]
        assert "id" in task
        assert "createdAt" in task
        assert task.get("groupId") is None

    def test_create_group_task_success(self, base_url, valid_group_task_data):
        """Test successful creation of a group task"""
        response = requests.post(base_url + ENDPOINT_TASKS, json=valid_group_task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["title"] == valid_group_task_data["title"]
        assert task["groupId"] == valid_group_task_data["groupId"]
        assert "id" in task
        assert "createdAt" in task

    def test_create_task_with_doer(self, base_url, valid_task_data, second_authorized_user):
        """Test creating a task with a doer assigned"""
        task_data = valid_task_data.copy()
        task_data["doerId"] = second_authorized_user.get("userId")

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["doerId"] == second_authorized_user.get("userId")

    def test_create_task_with_priority(self, base_url, valid_task_data):
        """Test creating a task with explicit priority"""
        task_data = valid_task_data.copy()
        task_data["priority"] = "HIGH"

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["priority"] == "HIGH"

    def test_create_task_default_priority(self, base_url, valid_task_data):
        """Test that default priority is MIDDLE when not provided"""
        task_data = valid_task_data.copy()
        if "priority" in task_data:
            del task_data["priority"]

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["priority"] == "MIDDLE"

    def test_create_task_missing_title(self, base_url, valid_task_data):
        """Test creating a task without a title"""
        task_data = valid_task_data.copy()
        del task_data["title"]

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 400

    def test_create_task_empty_title(self, base_url, valid_task_data):
        """Test creating a task with empty title"""
        task_data = valid_task_data.copy()
        task_data["title"] = ""

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 400

    def test_create_task_missing_description(self, base_url, valid_task_data):
        """Test creating a task without a description"""
        task_data = valid_task_data.copy()
        del task_data["description"]

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 400

    def test_create_task_missing_author(self, base_url, valid_task_data):
        """Test creating a task without an authorId"""
        task_data = valid_task_data.copy()
        del task_data["authorId"]

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 400

    def test_create_task_missing_location(self, base_url, valid_task_data):
        """Test creating a task without location (location is optional)"""
        task_data = valid_task_data.copy()
        del task_data["location"]

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201

    @pytest.mark.parametrize("latitude,longitude",
                             [
                                 (-100, 40),
                                 (100, 40),
                                 (40, -200),
                                 (40, 200),
                                 (-100, 400),
                                 (100, 500)
                             ])
    def test_create_task_invalid_location_coordinates(self, base_url, valid_task_data, latitude, longitude):
        """Test creating a task with invalid latitude/longitude"""
        task_data = valid_task_data.copy()
        task_data["location"]["latitude"] = latitude  # latitude should be from -90 to 90
        task_data["location"]["longitude"] = longitude  # longitude should be from -180 to 180

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 400

    def test_create_task_title_too_long(self, base_url, valid_task_data):
        """Test creating a task with title exceeding max length (200)"""
        task_data = valid_task_data.copy()
        task_data["title"] = "A" * 201  # Max is 200

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 400

    def test_create_task_description_too_long(self, base_url, valid_task_data):
        """Test creating a task with description exceeding max length (1000)"""
        task_data = valid_task_data.copy()
        task_data["description"] = "A" * 1001  # Max is 1000

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 400


class TestTaskRetrieval:
    """Tests for retrieving tasks"""

    def test_get_task_by_id_success(self, base_url, created_task):
        """Test retrieving a task by ID"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        task = response.json()
        assert task["id"] == created_task["id"]
        assert task["title"] == created_task["title"]
        assert "status" in task  # Added: verify status field
        assert "priority" in task  # Added: verify priority field

    def test_get_task_by_id_not_found(self, base_url):
        """Test retrieving a non-existent task"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=99999)
        response = requests.get(base_url + endpoint)

        assert response.status_code == 404

    def test_get_personal_tasks_by_user(self, base_url, created_task, registered_authorized_user):
        """Test retrieving all personal tasks for a user"""
        endpoint = ENDPOINT_PERSONAL_TASKS.format(userId=registered_authorized_user.get("userId"))
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        # Check if our created task is in the list
        task_ids = [task["id"] for task in tasks]
        assert created_task["id"] in task_ids

    def test_get_tasks_by_author(self, base_url, created_task, registered_authorized_user):
        """Test retrieving all tasks created by a user"""
        endpoint = ENDPOINT_USER_TASKS.format(userId=registered_authorized_user.get("userId"))
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        task_ids = [task["id"] for task in tasks]
        assert created_task["id"] in task_ids

    def test_get_tasks_by_doer(self, base_url, valid_task_data, second_authorized_user):
        """Test retrieving all tasks assigned to a user"""
        # Create a task with a doer
        task_data = valid_task_data.copy()
        task_data["doerId"] = second_authorized_user.get("userId")
        create_response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)
        assert create_response.status_code == 201
        created_task = create_response.json()

        # Retrieve tasks by doer
        endpoint = f'/tasks/doer/{second_authorized_user.get("userId")}'
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        task_ids = [task["id"] for task in tasks]
        assert created_task["id"] in task_ids

    def test_get_group_tasks(self, base_url, created_group_task):
        """Test retrieving all tasks for a specific group"""
        endpoint = ENDPOINT_GROUP_TASKS.format(groupId=created_group_task["groupId"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        task_ids = [task["id"] for task in tasks]
        assert created_group_task["id"] in task_ids


class TestTaskUpdate:
    """Tests for updating tasks"""

    def test_update_task_title(self, base_url, created_task):
        """Test updating a task's title"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "title": "Updated Task Title"
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["title"] == "Updated Task Title"
        assert updated_task["id"] == created_task["id"]

    def test_update_task_description(self, base_url, created_task):
        """Test updating a task's description"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "description": "Updated task description"
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["description"] == "Updated task description"

    def test_update_task_status(self, base_url, created_task):
        """Test updating a task's status"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "status": "DONE"
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["status"] == "DONE"

    def test_update_task_priority(self, base_url, created_task):
        """Test updating a task's priority"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "priority": "HIGH"
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["priority"] == "HIGH"

    def test_update_task_doer(self, base_url, created_task, second_authorized_user):
        """Test updating a task's doer"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "doerId": second_authorized_user.get("userId")
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["doerId"] == second_authorized_user.get("userId")

    def test_update_task_location(self, base_url, created_task):
        """Test updating a task's location"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "location": {
                "latitude": 51.5074,
                "longitude": -0.1278,
                "name": "London",
                "remindByLocation": False
            }
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["location"]["name"] == "London"

    def test_update_task_deadline(self, base_url, created_task):
        """Test updating a task's deadline"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        new_deadline = datetime.utcnow() + timedelta(days=14)
        update_data = {
            "deadline": {
                "time": new_deadline.isoformat() + "Z",
                "remindByTime": False
            }
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["deadline"]["remindByTime"] is False

    def test_update_nonexistent_task(self, base_url):
        """Test updating a non-existent task"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=99999)
        update_data = {
            "title": "This should fail"
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 404

    def test_update_task_invalid_title_length(self, base_url, created_task):
        """Test updating a task with invalid title length (max 200)"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "title": "A" * 201  # Exceeds max length of 200
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 400

    def test_update_task_empty_title(self, base_url, created_task):
        """Test updating a task with empty title"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        update_data = {
            "title": ""
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 400


class TestTaskDeletion:
    """Tests for deleting tasks"""

    def test_delete_task_success(self, base_url, created_task):
        """Test deleting a task"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        response = requests.delete(base_url + endpoint)

        assert response.status_code == 204

        # Verify task is deleted
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 404

    def test_delete_nonexistent_task(self, base_url):
        """Test deleting a non-existent task"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=99999)
        response = requests.delete(base_url + endpoint)

        assert response.status_code == 404
