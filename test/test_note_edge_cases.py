import pytest
import requests
from .conftest import ENDPOINT_NOTES, ENDPOINT_NOTE_BY_ID


class TestNoteEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def test_create_note_with_all_optional_fields(self, base_url, registered_authorized_user):
        """Test creating a note with all optional fields populated"""
        note_data = {
            "title": "Complete Note",
            "description": "Note with all fields",
            "groupId": 42,
            "authorId": registered_authorized_user.get("userId"),
            "location": {
                "latitude": 48.8566,
                "longitude": 2.3522,
                "name": "Paris",
                "remindByLocation": True
            }
        }

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 201
        note = response.json()
        assert note["title"] == note_data["title"]
        assert note["groupId"] == 42
        assert note["location"]["name"] == "Paris"

    @pytest.mark.parametrize("latitude", [-90, -45, 0, 45, 90])
    def test_create_note_boundary_latitude_values(self, base_url, valid_note_data, latitude):
        """Test creating notes with boundary and various latitude values"""
        note_data = valid_note_data.copy()
        note_data["location"]["latitude"] = latitude

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 201
        note = response.json()
        assert note["location"]["latitude"] == latitude

    @pytest.mark.parametrize("longitude", [-180, -90, 0, 90, 180])
    def test_create_note_boundary_longitude_values(self, base_url, valid_note_data, longitude):
        """Test creating notes with boundary and various longitude values"""
        note_data = valid_note_data.copy()
        note_data["location"]["longitude"] = longitude

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 201
        note = response.json()
        assert note["location"]["longitude"] == longitude

    @pytest.mark.parametrize("location_data", [
        {"latitude": 40.7128, "longitude": -74.0060, "name": "New York", "remindByLocation": True},
        {"latitude": 51.5074, "longitude": -0.1278, "name": "London", "remindByLocation": False},
        {"latitude": 35.6762, "longitude": 139.6503, "name": "Tokyo", "remindByLocation": True},
        {"latitude": -33.8688, "longitude": 151.2093, "name": "Sydney", "remindByLocation": False},
        {"latitude": 55.7558, "longitude": 37.6173, "name": "Moscow", "remindByLocation": True},
    ])
    def test_create_note_various_locations(self, base_url, valid_note_data, location_data):
        """Test creating notes with various valid locations"""
        note_data = valid_note_data.copy()
        note_data["location"] = location_data

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 201
        note = response.json()
        assert note["location"]["name"] == location_data["name"]
        assert note["location"]["latitude"] == location_data["latitude"]
        assert note["location"]["longitude"] == location_data["longitude"]
        assert note["location"]["remindByLocation"] == location_data["remindByLocation"]

    @pytest.mark.parametrize("length", [1, 50, 100, 150, 200])
    def test_create_note_title_lengths(self, base_url, valid_note_data, length):
        """Test creating notes with various valid title lengths"""
        note_data = valid_note_data.copy()
        note_data["title"] = "A" * length

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 201
        note = response.json()
        assert len(note["title"]) == length

    @pytest.mark.parametrize("length", [1, 250, 500, 750, 1000])
    def test_create_note_description_lengths(self, base_url, valid_note_data, length):
        """Test creating notes with various valid description lengths"""
        note_data = valid_note_data.copy()
        note_data["description"] = "B" * length

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 201
        note = response.json()
        assert len(note["description"]) == length

    @pytest.mark.parametrize("remind_by_location", [True, False])
    def test_create_note_location_reminder_flag(self, base_url, valid_note_data, remind_by_location):
        """Test creating notes with different location reminder flags"""
        note_data = valid_note_data.copy()
        note_data["location"]["remindByLocation"] = remind_by_location

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 201
        note = response.json()
        assert note["location"]["remindByLocation"] == remind_by_location

    def test_update_note_location(self, base_url, created_note):
        """Test updating a note's location"""
        endpoint = ENDPOINT_NOTE_BY_ID.format(noteId=created_note["id"])
        new_location = {
            "latitude": 48.8566,
            "longitude": 2.3522,
            "name": "Paris",
            "remindByLocation": False
        }
        update_data = {"location": new_location}

        response = requests.put(base_url + endpoint, json=update_data)

        assert response.status_code == 200
        updated_note = response.json()
        assert updated_note["location"]["name"] == "Paris"
        assert updated_note["location"]["latitude"] == 48.8566
        assert updated_note["location"]["longitude"] == 2.3522
        assert updated_note["location"]["remindByLocation"] is False

    def test_create_note_minimal_data(self, base_url, registered_authorized_user):
        """Test creating a note with only required fields"""
        note_data = {
            "title": "Minimal Note",
            "description": "Just the basics",
            "authorId": registered_authorized_user.get("userId")
        }

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 201
        note = response.json()
        assert note["title"] == note_data["title"]
        assert note["description"] == note_data["description"]
        assert note["authorId"] == note_data["authorId"]
        assert note.get("groupId") is None
        assert note.get("location") is None

    def test_create_multiple_notes_same_author(self, base_url, registered_authorized_user):
        """Test creating multiple notes by the same author"""
        note_ids = []

        for i in range(3):
            note_data = {
                "title": f"Note {i + 1}",
                "description": f"Description for note {i + 1}",
                "authorId": registered_authorized_user.get("userId")
            }
            response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)
            assert response.status_code == 201
            note = response.json()
            note_ids.append(note["id"])

        # Verify all notes are unique
        assert len(note_ids) == len(set(note_ids))

        # Verify all notes are retrievable
        from .conftest import ENDPOINT_USER_NOTES
        endpoint = ENDPOINT_USER_NOTES.format(userId=registered_authorized_user.get("userId"))
        response = requests.get(base_url + endpoint)
        assert response.status_code == 200
        notes = response.json()
        retrieved_note_ids = [note["id"] for note in notes]

        for note_id in note_ids:
            assert note_id in retrieved_note_ids

    def test_create_group_note_with_location(self, base_url, registered_authorized_user):
        """Test creating a group note with location"""
        note_data = {
            "title": "Group Note with Location",
            "description": "A group note that has location data",
            "authorId": registered_authorized_user.get("userId"),
            "groupId": 123,
            "location": {
                "latitude": 37.7749,
                "longitude": -122.4194,
                "name": "San Francisco",
                "remindByLocation": True
            }
        }

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 201
        note = response.json()
        assert note["groupId"] == 123
        assert note["location"]["name"] == "San Francisco"
        assert note["location"]["remindByLocation"] is True

    @pytest.mark.parametrize("location_name_length", [1, 50, 100, 150, 200])
    def test_create_note_location_name_lengths(self, base_url, valid_note_data, location_name_length):
        """Test creating notes with various location name lengths"""
        note_data = valid_note_data.copy()
        note_data["location"]["name"] = "L" * location_name_length

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 201
        note = response.json()
        assert len(note["location"]["name"]) == location_name_length

    def test_create_note_location_name_too_long(self, base_url, valid_note_data):
        """Test creating a note with location name exceeding max length (200)"""
        note_data = valid_note_data.copy()
        note_data["location"]["name"] = "L" * 500

        response = requests.post(base_url + ENDPOINT_NOTES, json=note_data)

        assert response.status_code == 400