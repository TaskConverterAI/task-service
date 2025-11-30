import random
import string
import requests
import pytest
from datetime import datetime, timedelta

# API Endpoints
ENDPOINT_TASKS = '/tasks'
ENDPOINT_TASK_BY_ID = '/tasks/{taskId}'
ENDPOINT_TASK_COMMENT = '/tasks/{taskId}/comment'
ENDPOINT_COMMENT_DELETE = '/tasks/comment/{commentId}'
ENDPOINT_PERSONAL_TASKS = '/tasks/personal/{userId}'
ENDPOINT_USER_TASKS = '/tasks/user/{userId}'
ENDPOINT_DOER_TASKS = '/tasks/doer/{doerId}'
ENDPOINT_GROUP_TASKS = '/tasks/group/{groupId}'
ENDPOINT_TASK_DETAILS = '/tasks/details/{taskId}'
ENDPOINT_ADD_SUBTASK = '/tasks/{taskId}/subtask'
ENDPOINT_UPDATE_SUBTASK_STATUS = '/tasks/subtasks/{subtaskId}/status'

@pytest.fixture
def random_user_id():
    """Generates a random user ID"""
    return random.randint(1, 100000)


@pytest.fixture
def second_user_id():
    """Generates a second random user ID"""
    return random.randint(100001, 200000)


@pytest.fixture
def registered_authorized_user(random_user_id):
    """Generates user data with random userId"""
    username = "user_" + ''.join(random.choices(string.ascii_lowercase, k=6))
    return {
        "username": username,
        "email": f"{username}@example.com",
        "userId": random_user_id
    }


@pytest.fixture
def second_authorized_user(second_user_id):
    """Generates second user data with random userId"""
    username = "user_" + ''.join(random.choices(string.ascii_lowercase, k=6))
    return {
        "username": username,
        "email": f"{username}@example.com",
        "userId": second_user_id
    }


@pytest.fixture
def valid_location_data():
    """Generates valid location data"""
    return {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "name": "New York City",
        "remindByLocation": True
    }


@pytest.fixture
def valid_deadline_data():
    """Generates valid deadline data"""
    future_time = datetime.utcnow() + timedelta(days=7)
    return {
        "time": future_time.isoformat() + "Z",
        "remindByTime": True
    }


@pytest.fixture
def valid_task_data(registered_authorized_user, valid_location_data, valid_deadline_data):
    """Generates valid task creation data"""
    return {
        "title": "Test Task " + ''.join(random.choices(string.ascii_letters, k=6)),
        "description": "This is a test task description",
        "authorId": registered_authorized_user.get("userId"),
        "location": valid_location_data,
        "deadline": valid_deadline_data
    }


@pytest.fixture
def valid_group_task_data(registered_authorized_user, valid_location_data, valid_deadline_data):
    """Generates valid group task creation data"""
    return {
        "title": "Group Task " + ''.join(random.choices(string.ascii_letters, k=6)),
        "description": "This is a group task description",
        "authorId": registered_authorized_user.get("userId"),
        "groupId": random.randint(1, 100),
        "location": valid_location_data,
        "deadline": valid_deadline_data
    }


@pytest.fixture
def created_task(base_url, valid_task_data):
    """Creates a task and returns the task data"""
    response = requests.post(base_url + ENDPOINT_TASKS, json=valid_task_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def created_group_task(base_url, valid_group_task_data):
    """Creates a group task and returns the task data"""
    response = requests.post(base_url + ENDPOINT_TASKS, json=valid_group_task_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def task_with_subtask(base_url, created_task):
    """Creates a task with a subtask"""
    subtask_data = {
        "text": "Test subtask description"
    }
    endpoint = ENDPOINT_ADD_SUBTASK.format(taskId=created_task["id"])
    response = requests.post(base_url + endpoint, json=subtask_data)
    assert response.status_code == 201
    subtask = response.json()
    return {
        "task": created_task,
        "subtask": subtask
    }


@pytest.fixture
def task_with_comment(base_url, created_task, registered_authorized_user):
    """Creates a task with a comment"""
    comment_data = {
        "authorId": registered_authorized_user.get("userId"),
        "text": "This is a test comment"
    }
    endpoint = ENDPOINT_TASK_COMMENT.format(taskId=created_task["id"])
    response = requests.put(base_url + endpoint, json=comment_data)
    assert response.status_code == 200
    comment = response.json()
    return {
        "task": created_task,
        "comment": comment
    }
