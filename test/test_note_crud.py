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
    """Tests for updating notes with verification"""

    def test_update_note_title(self, base_url, created_note):
        """Test updating a note's title and verify persistence"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        update_data = {
            "title": "Updated Note Title"
        }

        # Update the note
        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 200
        updated_note = update_response.json()
        assert updated_note["title"] == "Updated Note Title"
        assert updated_note["id"] == created_note["id"]

        # Verify the update persisted
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 200
        retrieved_note = get_response.json()
        assert retrieved_note["title"] == "Updated Note Title"
        assert retrieved_note["id"] == created_note["id"]

    def test_update_note_description(self, base_url, created_note):
        """Test updating a note's description and verify persistence"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        update_data = {
            "description": "Updated note description"
        }

        # Update the note
        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 200
        updated_note = update_response.json()
        assert updated_note["description"] == "Updated note description"

        # Verify the update persisted
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 200
        retrieved_note = get_response.json()
        assert retrieved_note["description"] == "Updated note description"

    def test_update_note_location(self, base_url, created_note):
        """Test updating a note's location and verify persistence"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        update_data = {
            "location": {
                "latitude": 51.5074,
                "longitude": -0.1278,
                "name": "London",
                "remindByLocation": False
            }
        }

        # Update the note
        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 200
        updated_note = update_response.json()
        assert updated_note["location"]["name"] == "London"
        assert updated_note["location"]["latitude"] == 51.5074
        assert updated_note["location"]["longitude"] == -0.1278
        assert updated_note["location"]["remindByLocation"] is False

        # Verify the update persisted
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 200
        retrieved_note = get_response.json()
        assert retrieved_note["location"]["name"] == "London"
        assert retrieved_note["location"]["latitude"] == 51.5074
        assert retrieved_note["location"]["longitude"] == -0.1278
        assert retrieved_note["location"]["remindByLocation"] is False

    def test_update_nonexistent_note(self, base_url):
        """Test updating a non-existent note"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=99999)
        update_data = {
            "title": "This should fail"
        }

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 404

    def test_update_note_empty_title(self, base_url, created_note):
        """Test updating a note with empty title"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        original_title = created_note["title"]

        update_data = {
            "title": ""
        }

        # Update should fail
        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 400

        # Verify original title is unchanged
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 200
        retrieved_note = get_response.json()
        assert retrieved_note["title"] == original_title

    @pytest.mark.parametrize("update_fields", [
        {"title": "Updated Title", "description": "Updated Description"},
        {"title": "New Title", "location": {"latitude": 40.7128, "longitude": -74.0060, "name": "NYC", "remindByLocation": True}},
    ])
    def test_update_multiple_fields_simultaneously(self, base_url, created_note, update_fields):
        """Test updating multiple note fields in one request and verify persistence"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])

        # Update the note
        update_response = requests.put(base_url + endpoint, json=update_fields)
        assert update_response.status_code == 200
        updated_note = update_response.json()

        # Verify fields in update response
        if "title" in update_fields:
            assert updated_note["title"] == update_fields["title"]
        if "description" in update_fields:
            assert updated_note["description"] == update_fields["description"]
        if "location" in update_fields:
            assert updated_note["location"]["name"] == update_fields["location"]["name"]

        # Verify the updates persisted
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 200
        retrieved_note = get_response.json()

        # Verify all fields persisted
        if "title" in update_fields:
            assert retrieved_note["title"] == update_fields["title"]
        if "description" in update_fields:
            assert retrieved_note["description"] == update_fields["description"]
        if "location" in update_fields:
            assert retrieved_note["location"]["name"] == update_fields["location"]["name"]
            assert retrieved_note["location"]["latitude"] == update_fields["location"]["latitude"]
            assert retrieved_note["location"]["longitude"] == update_fields["location"]["longitude"]

    @pytest.mark.parametrize("field,value", [
        ("title", "Parametrized Title Update"),
        ("description", "Parametrized Description Update"),
    ])
    def test_update_single_field_parametrized(self, base_url, created_note, field, value):
        """Test updating individual fields and verify persistence"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        update_data = {field: value}

        # Update the note
        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 200
        updated_note = update_response.json()
        assert updated_note[field] == value

        # Verify the update persisted
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 200
        retrieved_note = get_response.json()
        assert retrieved_note[field] == value

    def test_update_preserves_other_fields(self, base_url, created_note):
        """Test that updating one field doesn't affect other fields"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])

        # Store original values
        original_description = created_note["description"]
        original_author_id = created_note["authorId"]

        # Update only the title
        update_data = {
            "title": "Only Title Updated"
        }

        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 200

        # Verify other fields are preserved
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 200
        retrieved_note = get_response.json()

        assert retrieved_note["title"] == "Only Title Updated"
        assert retrieved_note["description"] == original_description
        assert retrieved_note["authorId"] == original_author_id

    def test_sequential_updates(self, base_url, created_note):
        """Test multiple sequential updates and verify each persists"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])

        # First update: title
        update_response_1 = requests.put(base_url + endpoint, json={"title": "First Update"})
        assert update_response_1.status_code == 200

        get_response_1 = requests.get(base_url + endpoint)
        assert get_response_1.status_code == 200
        assert get_response_1.json()["title"] == "First Update"

        # Second update: description
        update_response_2 = requests.put(base_url + endpoint, json={"description": "Second Update"})
        assert update_response_2.status_code == 200

        get_response_2 = requests.get(base_url + endpoint)
        assert get_response_2.status_code == 200
        retrieved_note = get_response_2.json()
        assert retrieved_note["title"] == "First Update"  # Previous update should persist
        assert retrieved_note["description"] == "Second Update"

        # Third update: location
        new_location = {
            "latitude": 35.6762,
            "longitude": 139.6503,
            "name": "Tokyo",
            "remindByLocation": True
        }
        update_response_3 = requests.put(base_url + endpoint, json={"location": new_location})
        assert update_response_3.status_code == 200

        get_response_3 = requests.get(base_url + endpoint)
        assert get_response_3.status_code == 200
        final_note = get_response_3.json()
        assert final_note["title"] == "First Update"  # All previous updates should persist
        assert final_note["description"] == "Second Update"
        assert final_note["location"]["name"] == "Tokyo"

    def test_update_location_reminder_flag_only(self, base_url, created_note):
        """Test updating only the location reminder flag and verify persistence"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])

        # Get original location
        original_location = created_note.get("location")
        if not original_location:
            pytest.skip("Note doesn't have location")

        # Update only remindByLocation
        updated_location = original_location.copy()
        updated_location["remindByLocation"] = not original_location["remindByLocation"]

        update_response = requests.put(base_url + endpoint, json={"location": updated_location})
        assert update_response.status_code == 200

        # Verify the update persisted
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 200
        retrieved_note = get_response.json()

        assert retrieved_note["location"]["remindByLocation"] == updated_location["remindByLocation"]
        assert retrieved_note["location"]["name"] == original_location["name"]
        assert retrieved_note["location"]["latitude"] == original_location["latitude"]
        assert retrieved_note["location"]["longitude"] == original_location["longitude"]

    @pytest.mark.parametrize("invalid_length", [1001, 1500, 2000])
    def test_update_note_invalid_description_length(self, base_url, created_note, invalid_length):
        """Test updating a note with invalid description length (max 1000)"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        original_description = created_note["description"]

        update_data = {
            "description": "B" * invalid_length
        }

        # Update should fail
        update_response = requests.put(base_url + endpoint, json=update_data)
        assert update_response.status_code == 400

        # Verify original description is unchanged
        get_response = requests.get(base_url + endpoint)
        assert get_response.status_code == 200
        retrieved_note = get_response.json()
        assert retrieved_note["description"] == original_description
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