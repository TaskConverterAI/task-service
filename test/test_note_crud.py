import pytest
import requests
from .conftest import (
    ENDPOINT_NOTES,
    ENDPOINT_NOTE_BY_ID,
    ENDPOINT_PERSONAL_NOTES,
    ENDPOINT_USER_NOTES,
    ENDPOINT_GROUP_NOTES
)


class TestNoteCreation:
    """Tests for creating notes"""

    def test_create_personal_note_success(self, base_url, valid_note_data):
        """Test successful creation of a personal note"""
        response = requests.post(base_url + ENDPOINT_NOTES, json=valid_note_data)

        assert response.status_code == 201
        note = response.json()
        assert note["title"] == valid_note_data["title"]
        assert note["description"] == valid_note_data["description"]
        assert note["authorId"] == valid_note_data["authorId"]
        assert "id" in note
        assert "createdAt" in note
        assert note.get("groupId") is None

    def test_create_group_note_success(self, base_url, valid_group_note_data):
        """Test successful creation of a group note"""
        response = requests.post(base_url + ENDPOINT_NOTES, json=valid_group_note_data)

        assert response.status_code == 201
        note = response.json()
        assert note["title"] == valid_group_note_data["title"]
        assert note["groupId"] == valid_group_note_data["groupId"]
        assert "id" in note
        assert "createdAt" in note

    def test_create_note_with_location(self, base_url, valid_note_data):
        """Test creating a note with location data"""
        response = requests.post(base_url + ENDPOINT_NOTES, json=valid_note_data)

        assert response.status_code == 201
        note = response.json()
        assert "location" in note
        assert note["location"]["name"] == valid_note_data["location"]["name"]

    @pytest.mark.parametrize("missing_field", ["title", "authorId"])
    def test_create_note_missing_required_field(self, base_url, valid_note_data, missing_field):
        """Test creating a note without required fields"""
        note_data = valid_note_data.copy()
        del note_data[missing_field]

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 400

    def test_create_note_empty_title(self, base_url, valid_note_data):
        """Test creating a note with empty title"""
        note_data = valid_note_data.copy()
        note_data["title"] = ""

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 400

    def test_create_note_missing_location(self, base_url, valid_note_data):
        """Test creating a note without location (location is optional)"""
        note_data = valid_note_data.copy()
        del note_data["location"]

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

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
    def test_create_note_invalid_location_coordinates(self, base_url, valid_note_data, latitude, longitude):
        """Test creating a note with invalid latitude/longitude"""
        note_data = valid_note_data.copy()
        note_data["location"]["latitude"] = latitude
        note_data["location"]["longitude"] = longitude

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 400

    @pytest.mark.parametrize("length", [300])
    def test_create_note_title_too_long(self, base_url, valid_note_data, length):
        """Test creating a note with title exceeding max length (200)"""
        note_data = valid_note_data.copy()
        note_data["title"] = "A" * length

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 400

class TestNoteRetrieval:
    """Tests for retrieving notes"""

    def test_get_note_by_id_success(self, base_url, created_note):
        """Test retrieving a note by ID"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        note = response.json()
        assert note["id"] == created_note["id"]
        assert note["title"] == created_note["title"]

    def test_get_note_by_id_not_found(self, base_url):
        """Test retrieving a non-existent note"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=99999)
        response = requests.get(base_url + endpoint)

        assert response.status_code == 404

    def test_get_personal_notes_by_user(self, base_url, created_note, registered_authorized_user):
        """Test retrieving all personal notes for a user"""
        endpoint = ENDPOINT_PERSONAL_NOTES.format(userId=registered_authorized_user.get("userId"))
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        notes = response.json()
        assert isinstance(notes, list)
        note_ids = [note["id"] for note in notes]
        assert created_note["id"] in note_ids

    def test_get_notes_by_author(self, base_url, created_note, registered_authorized_user):
        """Test retrieving all notes created by a user"""
        endpoint = ENDPOINT_USER_NOTES.format(userId=registered_authorized_user.get("userId"))
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        notes = response.json()
        assert isinstance(notes, list)
        note_ids = [note["id"] for note in notes]
        assert created_note["id"] in note_ids

    def test_get_group_notes(self, base_url, created_group_note):
        """Test retrieving all notes for a specific group"""
        endpoint = ENDPOINT_GROUP_NOTES.format(groupId=created_group_note["groupId"])
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        notes = response.json()
        assert isinstance(notes, list)
        note_ids = [note["id"] for note in notes]
        assert created_group_note["id"] in note_ids

    @pytest.mark.parametrize("endpoint_template,user_id", [
        (ENDPOINT_PERSONAL_NOTES, 999999),
        (ENDPOINT_USER_NOTES, 999999),
    ])
    def test_get_notes_empty_list_for_nonexistent_user(self, base_url, endpoint_template, user_id):
        """Test getting notes for user with no notes returns empty list"""
        endpoint = endpoint_template.format(userId=user_id)
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        notes = response.json()
        assert isinstance(notes, list)
        assert len(notes) == 0

    def test_get_group_notes_empty_list(self, base_url):
        """Test getting notes for group with no notes"""
        non_existent_group_id = 999999
        endpoint = ENDPOINT_GROUP_NOTES.format(groupId=non_existent_group_id)
        response = requests.get(base_url + endpoint)

        assert response.status_code == 200
        notes = response.json()
        assert isinstance(notes, list)
        assert len(notes) == 0


class TestNoteUpdate:
    """Tests for updating notes"""

    def test_update_note_title(self, base_url, created_note):
        """Test updating a note's title"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        update_data = {
            "title": "Updated Note Title"
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_note = response.json()
        assert updated_note["title"] == "Updated Note Title"
        assert updated_note["id"] == created_note["id"]

    def test_update_note_description(self, base_url, created_note):
        """Test updating a note's description"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        update_data = {
            "description": "Updated note description"
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_note = response.json()
        assert updated_note["description"] == "Updated note description"

    def test_update_note_location(self, base_url, created_note):
        """Test updating a note's location"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
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
        updated_note = response.json()
        assert updated_note["location"]["name"] == "London"

    def test_update_nonexistent_note(self, base_url):
        """Test updating a non-existent note"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=99999)
        update_data = {
            "title": "This should fail"
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 404

    @pytest.mark.parametrize("length", [300, 1500])
    def test_update_note_invalid_title_length(self, base_url, created_note, length):
        """Test updating a note with invalid title length (max 200)"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        update_data = {
            "title": "A" * length
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 400

    def test_update_note_empty_title(self, base_url, created_note):
        """Test updating a note with empty title"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        update_data = {
            "title": ""
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 400

    @pytest.mark.parametrize("update_fields", [
        {"title": "Updated Title", "description": "Updated Description"},
        {"title": "New Title", "location": {"latitude": 40.7128, "longitude": -74.0060, "name": "NYC", "remindByLocation": True}},
    ])
    def test_update_multiple_fields_simultaneously(self, base_url, created_note, update_fields):
        """Test updating multiple note fields in one request"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])

        response = requests.put(base_url + endpoint, json=update_fields)

        assert response.status_code == 200
        updated_note = response.json()

        if "title" in update_fields:
            assert updated_note["title"] == update_fields["title"]
        if "description" in update_fields:
            assert updated_note["description"] == update_fields["description"]
        if "location" in update_fields:
            assert updated_note["location"]["name"] == update_fields["location"]["name"]


class TestNoteDeletion:
    """Tests for deleting notes"""

    def test_delete_note_success(self, base_url, created_note):
        """Test deleting a note"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        response = requests.delete(base_url + endpoint)

        assert response.status_code == 204

        # Verify note is deleted
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 404

    def test_delete_nonexistent_note(self, base_url):
        """Test deleting a non-existent note"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=99999)
        response = requests.delete(base_url + endpoint)

        assert response.status_code == 404