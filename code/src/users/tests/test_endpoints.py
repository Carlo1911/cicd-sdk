from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user(user):
    response = client.post(
        "/users",
        json=user,
    )
    assert response.status_code == 200
    assert response.json() == user


def test_create_user_minimal_data(user_minimal):
    response = client.post(
        "/users",
        json=user_minimal,
    )
    assert response.status_code == 200
    assert response.json() == user_minimal


def test_get_user(user):
    response = client.get(f"/users/{user['uid']}")
    assert response.status_code == 200
    assert response.json() == user


def test_get_non_existent_user():
    response = client.get("/users/987654321")
    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == "User not found"


def test_update_user_minimal_data(user_minimal, user_minimal_with_updates):
    response = client.patch(
        f"/users/{user_minimal['uid']}",
        json=user_minimal_with_updates,
    )
    assert response.status_code == 200
    assert response.json() == user_minimal_with_updates


def test_update_user(user, user_with_updates):
    response = client.patch(
        f"/users/{user['uid']}",
        json=user_with_updates,
    )
    assert response.status_code == 200
    assert response.json() == user_with_updates


def test_update_non_existent_user(user_with_updates):
    response = client.patch(
        "/users/987654321",
        json=user_with_updates,
    )
    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == "User not found"


def test_update_user_with_wrong_date_format(user, user_with_wrong_date_format):
    response = client.patch(
        f"/users/{user['uid']}",
        json=user_with_wrong_date_format,
    )
    json_response = response.json()
    assert response.status_code == 422
    assert (
        json_response["detail"][0]["msg"]
        == "Incorrect data format, should be YYYY-MM-DD"
    )


def test_wrong_size_social_security_nnumber(user_with_wrong_social_security_number):
    response = client.post(
        "/users",
        json=user_with_wrong_social_security_number,
    )
    json_response = response.json()
    assert response.status_code == 422
    assert (
        json_response["detail"][0]["msg"]
        == "ensure this value has at most 4 characters"
    )


def test_forbidden_extra_fields(user_with_extra_field):
    response = client.post(
        "/users",
        json=user_with_extra_field,
    )
    json_response = response.json()
    assert response.status_code == 422
    assert json_response["detail"][0]["msg"] == "extra fields not permitted"


def test_create_with_wrong_firebase_id_format(user_with_wrong_firebase_id_format):
    response = client.post(
        "/users",
        json=user_with_wrong_firebase_id_format,
    )
    json_response = response.json()
    assert response.status_code == 422
    assert (
        json_response["detail"][0]["msg"]
        == "Firebase ID must be contain at least one lowercase letter, one \
                    uppercase letter, and one number"
    )
