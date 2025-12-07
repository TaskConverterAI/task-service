import pytest
import requests
from .conftest import (
    ENDPOINT_TASK_COMMENT,
    ENDPOINT_COMMENT_DELETE,
    ENDPOINT_TASK_DETAILS
)

class TestTaskComments:
    """Tests for task comment operations"""

    def test_add_comment_to_task_success(self, base_url, created_task, registered_authorized_user):
        """Test adding a comment to a task"""
        comment_data = {
            "authorId": registered_authorized_user.get("userId"),
            "text": "This is a test comment"
        }
        endpoint = ENDPOINT_TASK_COMMENT.format(taskId=created_task["id"])
        response = requests.put(base_url + endpoint, json=comment_data)

        assert response.status_code == 200
        comment = response.json()
        assert comment["text"] == comment_data["text"]
        assert comment["authorId"] == comment_data["authorId"]
        assert "id" in comment
        assert "createdAt" in comment
        assert comment["taskId"] == created_task["id"]

    @pytest.mark.parametrize("missing_field", ["authorId", "text"])
    def test_add_comment_missing_required_field(self, base_url, created_task, registered_authorized_user, missing_field):
        """Test adding a comment without required fields"""
        comment_data = {
            "authorId": registered_authorized_user.get("userId"),
            "text": "This is a test comment"
        }
        del comment_data[missing_field]

        endpoint = ENDPOINT_TASK_COMMENT.format(taskId=created_task["id"])
        response = requests.put(base_url + endpoint, json=comment_data)

        assert response.status_code == 400

    def test_add_comment_to_nonexistent_task(self, base_url, registered_authorized_user):
        """Test adding a comment to non-existent task"""
        comment_data = {
            "authorId": registered_authorized_user.get("userId"),
            "text": "Comment on non-existent task"
        }
        endpoint = ENDPOINT_TASK_COMMENT.format(taskId=99999)
        response = requests.put(base_url + endpoint, json=comment_data)

        assert response.status_code == 404

    def test_add_multiple_comments_to_task(self, base_url, created_task, registered_authorized_user, second_authorized_user):
        """Test adding multiple comments to the same task"""
        # Add first comment
        comment_data_1 = {
            "authorId": registered_authorized_user.get("userId"),
            "text": "First comment"
        }
        endpoint = ENDPOINT_TASK_COMMENT.format(taskId=created_task["id"])
        response_1 = requests.put(base_url + endpoint, json=comment_data_1)
        assert response_1.status_code == 200
        comment_1 = response_1.json()

        # Add second comment
        comment_data_2 = {
            "authorId": second_authorized_user.get("userId"),
            "text": "Second comment"
        }
        response_2 = requests.put(base_url + endpoint, json=comment_data_2)
        assert response_2.status_code == 200
        comment_2 = response_2.json()

        # Verify both comments exist
        details_endpoint = ENDPOINT_TASK_DETAILS.format(taskId=created_task["id"])
        details_response = requests.get(base_url + details_endpoint)
        assert details_response.status_code == 200
        task_details = details_response.json()
        comment_ids = [c["id"] for c in task_details["comments"]]
        assert comment_1["id"] in comment_ids
        assert comment_2["id"] in comment_ids

    def test_delete_comment_success(self, base_url, task_with_comment):
        """Test deleting a comment"""
        comment_id = task_with_comment["comment"]["id"]
        endpoint = ENDPOINT_COMMENT_DELETE.format(commentId=comment_id)
        response = requests.delete(base_url + endpoint)

        assert response.status_code == 204

        # Verify comment is deleted by checking task details
        details_endpoint = ENDPOINT_TASK_DETAILS.format(taskId=task_with_comment["task"]["id"])
        details_response = requests.get(base_url + details_endpoint)
        assert details_response.status_code == 200
        task_details = details_response.json()
        comment_ids = [c["id"] for c in task_details["comments"]]
        assert comment_id not in comment_ids

    def test_delete_nonexistent_comment(self, base_url):
        """Test deleting a non-existent comment"""
        endpoint = ENDPOINT_COMMENT_DELETE.format(commentId=99999)
        response = requests.delete(base_url + endpoint)

        assert response.status_code == 404

    def test_comment_structure_in_task_details(self, base_url, task_with_comment):
        """Test that comments have correct structure in task details"""
        endpoint = ENDPOINT_TASK_DETAILS.format(taskId=task_with_comment["task"]["id"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        task_details = response.json()
        assert "comments" in task_details
        assert len(task_details["comments"]) > 0

        # Verify comment structure
        comment = task_details["comments"][0]
        required_fields = ["id", "taskId", "authorId", "text", "createdAt"]
        for field in required_fields:
            assert field in comment, f"Missing required field in comment: {field}"

    def test_add_comment_empty_text(self, base_url, created_task, registered_authorized_user):
        """Test adding a comment with empty text"""
        comment_data = {
            "authorId": registered_authorized_user.get("userId"),
            "text": ""
        }
        endpoint = ENDPOINT_TASK_COMMENT.format(taskId=created_task["id"])
        response = requests.put(base_url + endpoint, json=comment_data)

        # Should either accept empty text or return 400
        assert response.status_code in [200, 400]