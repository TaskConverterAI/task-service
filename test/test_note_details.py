import pytest
import requests
from .conftest import ENDPOINT_NOTE_DETAILS


class TestNoteDetails:
    """Tests for getting detailed note information"""

    def test_get_note_details_success(self, base_url, created_note):
        """Test retrieving detailed note information"""
        endpoint = ENDPOINT_NOTE_DETAILS.format(noteId=created_note["id"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        note_details = response.json()
        assert note_details["id"] == created_note["id"]
        assert note_details["title"] == created_note["title"]
        assert note_details["description"] == created_note["description"]
        assert "comments" in note_details
        assert isinstance(note_details["comments"], list)

    def test_get_note_details_with_comments(self, base_url, note_with_comment):
        """Test retrieving note details with comments"""
        endpoint = ENDPOINT_NOTE_DETAILS.format(noteId=note_with_comment["note"]["id"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        note_details = response.json()
        assert "comments" in note_details
        assert len(note_details["comments"]) > 0
        comment_ids = [c["id"] for c in note_details["comments"]]
        assert note_with_comment["comment"]["id"] in comment_ids

    def test_get_note_details_not_found(self, base_url):
        """Test retrieving details for non-existent note"""
        endpoint = ENDPOINT_NOTE_DETAILS.format(noteId=99999)
        response = requests.get(base_url + endpoint)

        assert response.status_code == 404

    def test_get_note_details_structure(self, base_url, created_note):
        """Test that note details response has correct structure"""
        endpoint = ENDPOINT_NOTE_DETAILS.format(noteId=created_note["id"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        note_details = response.json()

        # Verify all required fields are present
        required_fields = ["id", "title", "description", "authorId", "createdAt", "comments"]
        for field in required_fields:
            assert field in note_details, f"Missing required field: {field}"

    def test_get_note_details_with_location(self, base_url, valid_note_data):
        """Test retrieving note details with location data"""
        # Create note with location
        create_response = requests.post(base_url + "/tasks/note", json=valid_note_data)
        assert create_response.status_code == 201
        note = create_response.json()

        # Get note details
        endpoint = ENDPOINT_NOTE_DETAILS.format(noteId=note["id"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        note_details = response.json()
        assert "location" in note_details
        assert note_details["location"]["name"] == valid_note_data["location"]["name"]