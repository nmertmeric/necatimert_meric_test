import requests
import json
import pytest

# Base URL for the Petstore API
BASE_URL = "https://petstore.swagger.io/v2"

# Helper function to make API requests
def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    response = requests.request(method, url, headers=headers, data=json.dumps(data))
    return response

# Test data for a new pet
NEW_PET = {
    "id": 12345,
    "category": {"id": 1, "name": "Dogs"},
    "name": "Buddy",
    "photoUrls": ["https://example.com/buddy.jpg"],
    "tags": [{"id": 1, "name": "friendly"}],
    "status": "available"
}

# Positive Test: Create a new pet
def test_create_pet_positive():
    response = make_request("POST", "/pet", NEW_PET)
    assert response.status_code == 200
    assert response.json()["id"] == NEW_PET["id"]
    assert response.json()["name"] == NEW_PET["name"]

# Negative Test: Create a pet with invalid data (missing required field)
def test_create_pet_negative():
    invalid_pet = NEW_PET.copy()
    invalid_pet.pop("name")  # Remove required field
    response = make_request("POST", "/pet", invalid_pet)
    assert response.status_code == 200  # API returns 200 even for invalid data
    assert "name" not in response.json()  # Validate that the response does not include the missing field

# Positive Test: Get pet by ID
def test_get_pet_positive():
    pet_id = NEW_PET["id"]
    response = make_request("GET", f"/pet/{pet_id}")
    assert response.status_code == 200
    assert response.json()["id"] == pet_id

# Negative Test: Get pet with invalid ID
def test_get_pet_negative():
    invalid_pet_id = 999999  # Non-existent pet ID
    response = make_request("GET", f"/pet/{invalid_pet_id}")
    assert response.status_code == 404  # API returns 404 for invalid ID
    assert response.json().get("message") == "Pet not found"  # Validate the response message

# Positive Test: Update an existing pet
def test_update_pet_positive():
    updated_pet = NEW_PET.copy()
    updated_pet["name"] = "Max"
    response = make_request("PUT", "/pet", updated_pet)
    assert response.status_code == 200
    assert response.json()["name"] == "Max"

# Negative Test: Update a pet with invalid ID
def test_update_pet_negative():
    invalid_pet = NEW_PET.copy()
    invalid_pet["id"] = 999999  # Non-existent pet ID
    response = make_request("PUT", "/pet", invalid_pet)
    assert response.status_code == 200  # API returns 200 even for invalid ID
    assert response.json()["id"] == 999999  # Validate that the response includes the invalid ID

# Positive Test: Delete a pet
def test_delete_pet_positive():
    pet_id = NEW_PET["id"]
    response = make_request("DELETE", f"/pet/{pet_id}")
    assert response.status_code == 200

# Negative Test: Delete a pet with invalid ID
def test_delete_pet_negative():
    invalid_pet_id = 999999  # Non-existent pet ID
    response = make_request("DELETE", f"/pet/{invalid_pet_id}")
    assert response.status_code == 404  # API returns 404 for invalid ID
    assert response.json().get("message") == "Pet not found"  # Validate the response message

# Run the tests
if __name__ == "__main__":
    pytest.main()