import pytest
import requests
from datetime import datetime, timedelta
from .conftest import ENDPOINT_TASKS, ENDPOINT_TASK_BY_ID

class TestTaskEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def test_create_task_with_all_optional_fields(self, base_url, registered_authorized_user, second_authorized_user):
        """Test creating a task with all optional fields populated"""
        future_time = datetime.utcnow() + timedelta(days=10)
        task_data = {
            "title": "Complete Task",
            "description": "Task with all fields",
            "priority": "HIGH",
            "groupId": 42,
            "authorId": registered_authorized_user.get("userId"),
            "doerId": second_authorized_user.get("userId"),
            "location": {
                "latitude": 48.8566,
                "longitude": 2.3522,
                "name": "Paris",
                "remindByLocation": True
            },
            "deadline": {
                "time": future_time.isoformat() + "Z",
                "remindByTime": True
            }
        }

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["title"] == task_data["title"]
        assert task["priority"] == "HIGH"
        assert task["groupId"] == 42
        assert task["doerId"] == second_authorized_user.get("userId")
        assert task["location"]["name"] == "Paris"
        assert task["deadline"]["remindByTime"] is True

    @pytest.mark.parametrize("latitude", [-90, 0, 90])
    def test_create_task_boundary_latitude_values(self, base_url, valid_task_data, latitude):
        """Test creating tasks with boundary and middle latitude values"""
        task_data = valid_task_data.copy()
        task_data["location"]["latitude"] = latitude

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["location"]["latitude"] == latitude

    @pytest.mark.parametrize("longitude", [-180, 0, 180])
    def test_create_task_boundary_longitude_values(self, base_url, valid_task_data, longitude):
        """Test creating tasks with boundary and middle longitude values"""
        task_data = valid_task_data.copy()
        task_data["location"]["longitude"] = longitude

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["location"]["longitude"] == longitude

    @pytest.mark.parametrize("location_data", [
        {"latitude": 40.7128, "longitude": -74.0060, "name": "New York", "remindByLocation": True},
        {"latitude": 51.5074, "longitude": -0.1278, "name": "London", "remindByLocation": False},
        {"latitude": 35.6762, "longitude": 139.6503, "name": "Tokyo", "remindByLocation": True},
        {"latitude": -33.8688, "longitude": 151.2093, "name": "Sydney", "remindByLocation": False},
    ])
    def test_create_task_various_locations(self, base_url, valid_task_data, location_data):
        """Test creating tasks with various valid locations"""
        task_data = valid_task_data.copy()
        task_data["location"] = location_data

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["location"]["name"] == location_data["name"]
        assert task["location"]["latitude"] == location_data["latitude"]
        assert task["location"]["longitude"] == location_data["longitude"]
        assert task["location"]["remindByLocation"] == location_data["remindByLocation"]

    @pytest.mark.parametrize("length", [1, 100, 200])
    def test_create_task_title_lengths(self, base_url, valid_task_data, length):
        """Test creating tasks with various valid title lengths"""
        task_data = valid_task_data.copy()
        task_data["title"] = "A" * length

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert len(task["title"]) == length

    @pytest.mark.parametrize("update_fields", [
        {"title": "Updated Title", "description": "Updated Description"},
        {"status": "DONE", "priority": "LOW"},
        {"title": "New Title", "status": "DONE", "priority": "HIGH"},
    ])
    def test_update_multiple_fields_simultaneously(self, base_url, created_task, update_fields):
        """Test updating multiple task fields in one request"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])

        response = requests.put(base_url + endpoint, json=update_fields)

        assert response.status_code == 200
        updated_task = response.json()
        for field, value in update_fields.items():
            assert updated_task[field] == value

    @pytest.mark.parametrize("endpoint_template,user_id", [
        ("/tasks/personal/{userId}", 999999),
        ("/tasks/user/{userId}", 999999),
        ("/tasks/doer/{doerId}", 999999),
    ])
    def test_get_tasks_empty_list_for_nonexistent_user(self, base_url, endpoint_template, user_id):
        """Test getting tasks for user with no tasks returns empty list"""
        endpoint = endpoint_template.format(userId=user_id, doerId=user_id)
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        assert len(tasks) == 0

    def test_get_group_tasks_empty_list(self, base_url):
        """Test getting tasks for group with no tasks"""
        non_existent_group_id = 999999
        endpoint = f'/tasks/group/{non_existent_group_id}'
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        assert len(tasks) == 0

    @pytest.mark.parametrize("remind_by_location", [True, False])
    def test_create_task_location_reminder_flag(self, base_url, valid_task_data, remind_by_location):
        """Test creating tasks with different location reminder flags"""
        task_data = valid_task_data.copy()
        task_data["location"]["remindByLocation"] = remind_by_location

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["location"]["remindByLocation"] == remind_by_location

    @pytest.mark.parametrize("remind_by_time", [True, False])
    def test_create_task_deadline_reminder_flag(self, base_url, valid_task_data, remind_by_time):
        """Test creating tasks with different deadline reminder flags"""
        task_data = valid_task_data.copy()
        task_data["deadline"]["remindByTime"] = remind_by_time

        response = requests.post(base_url + ENDPOINT_TASKS, json=task_data)

        assert response.status_code == 201
        task = response.json()
        assert task["deadline"]["remindByTime"] == remind_by_time

    def test_update_task_location(self, base_url, created_task):
        """Test updating a task's location"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        new_location = {
            "latitude": 48.8566,
            "longitude": 2.3522,
            "name": "Paris",
            "remindByLocation": False
        }
        update_data = {"location": new_location}

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["location"]["name"] == "Paris"
        assert updated_task["location"]["latitude"] == 48.8566
        assert updated_task["location"]["longitude"] == 2.3522
        assert updated_task["location"]["remindByLocation"] is False

    def test_update_task_deadline(self, base_url, created_task):
        """Test updating a task's deadline"""
        endpoint = ENDPOINT_TASK_BY_ID.format(taskId=created_task["id"])
        new_deadline_time = datetime.utcnow() + timedelta(days=14)
        new_deadline = {
            "time": new_deadline_time.isoformat() + "Z",
            "remindByTime": False
        }
        update_data = {"deadline": new_deadline}

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["deadline"]["remindByTime"] is False