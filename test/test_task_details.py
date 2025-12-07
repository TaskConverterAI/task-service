import pytest
import requests
from .conftest import ENDPOINT_TASK_DETAILS

class TestTaskDetails:
    """Tests for getting detailed task information"""

    def test_get_task_details_success(self, base_url, created_task):
        """Test retrieving detailed task information"""
        endpoint = ENDPOINT_TASK_DETAILS.format(taskId=created_task["id"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        task_details = response.json()
        assert task_details["id"] == created_task["id"]
        assert task_details["title"] == created_task["title"]
        assert task_details["description"] == created_task["description"]
        assert "comments" in task_details
        assert isinstance(task_details["comments"], list)

    def test_get_task_details_with_comments(self, base_url, task_with_comment):
        """Test retrieving task details with comments"""
        endpoint = ENDPOINT_TASK_DETAILS.format(taskId=task_with_comment["task"]["id"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        task_details = response.json()
        assert "comments" in task_details
        assert len(task_details["comments"]) > 0
        comment_ids = [c["id"] for c in task_details["comments"]]
        assert task_with_comment["comment"]["id"] in comment_ids

    def test_get_task_details_not_found(self, base_url):
        """Test retrieving details for non-existent task"""
        endpoint = ENDPOINT_TASK_DETAILS.format(taskId=99999)
        response = requests.get(base_url + endpoint)

        assert response.status_code == 404

    def test_get_task_details_structure(self, base_url, created_task):
        """Test that task details response has correct structure"""
        endpoint = ENDPOINT_TASK_DETAILS.format(taskId=created_task["id"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        task_details = response.json()

        # Verify all required fields are present
        required_fields = ["id", "title", "description", "status", "priority",
                           "authorId", "createdAt", "comments"]
        for field in required_fields:
            assert field in task_details, f"Missing required field: {field}"