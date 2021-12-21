import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture()
def user():
    return {
        "uid": "45078f7613bf456a8b62497aa3febd83",
        "middleName": "Andre",
        "updatedAt": "2021-11-19",
        "dob": "1991-11-19",
        "firstName": "Carlo",
        "ssn": "123-11-1234",
        "addresses": {
            "mailing": {
                "city": "New York",
                "streetLine2": "Apt A",
                "state": "NY",
                "zipCode": "12345",
                "streetLine1": "123 Street",
            },
            "billing": {
                "city": "New York",
                "streetLine2": "Apt A",
                "state": "NY",
                "zipCode": "12345",
                "streetLine1": "123 Street",
            },
        },
        "phoneNumbers": {"home": "4448969", "cell": "0987654321"},
        "lastName": "Cohello",
        "createdAt": "2021-11-19",
    }


def test_create_user(user):
    response = client.post(
        "/users",
        json=user,
    )
    assert response.status_code == 200
    assert response.json() == user


def test_get_user(user):
    response = client.get(f"/users/{user['uid']}")
    assert response.status_code == 200
    assert response.json() == user


def test_update_user(user):
    update_user = {
        "uid": "45078f7613bf456a8b62497aa3febd83",
        "middleName": "Andre",
        "updatedAt": "2021-11-19",
        "dob": "1991-11-19",
        "firstName": "Carlo",
        "ssn": "123-11-1234",
        "addresses": {
            "mailing": {
                "city": "New York",
                "streetLine2": "Apt A",
                "state": "NY",
                "zipCode": "12345",
                "streetLine1": "123 Street",
            },
            "billing": {
                "city": "New York",
                "streetLine2": "Apt A",
                "state": "NY",
                "zipCode": "12345",
                "streetLine1": "123 Street",
            },
        },
        "phoneNumbers": {"home": "4448969", "cell": "0987654321"},
        "lastName": "Cohello",
        "createdAt": "2021-11-21",
    }
    response = client.patch(
        f"/users/{user['uid']}",
        json=update_user,
    )
    assert response.status_code == 200
    assert response.json() == update_user


def test_update_user_wrong_date_format(user):
    update_user = {
        "uid": "45078f7613bf456a8b62497aa3febd83",
        "middleName": "Andre",
        "updatedAt": "2021-11-19",
        "dob": "19/11/1991",
        "firstName": "Carlo",
        "ssn": "123-11-1234",
        "addresses": {
            "mailing": {
                "city": "New York",
                "streetLine2": "Apt A",
                "state": "NY",
                "zipCode": "12345",
                "streetLine1": "123 Street",
            },
            "billing": {
                "city": "New York",
                "streetLine2": "Apt A",
                "state": "NY",
                "zipCode": "12345",
                "streetLine1": "123 Street",
            },
        },
        "phoneNumbers": {"home": "4448969", "cell": "0987654321"},
        "lastName": "Cohello",
        "createdAt": "2021-11-21",
    }
    response = client.patch(
        f"/users/{user['uid']}",
        json=update_user,
    )
    assert response.status_code == 422
    json_response = response.json()
    assert (
        json_response["detail"][0]["msg"]
        == "Incorrect data format, should be YYYY-MM-DD"
    )
