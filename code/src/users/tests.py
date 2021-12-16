import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def user():
    return {
        "UID": "45078f7613bf456a8b62497aa3febd83",
        "MiddleName": "Andre",
        "UpdatedAt": "2021-11-19",
        "DOB": "1991-11-19",
        "FirstName": "Carlo",
        "SSN": "123-11-1234",
        "Addresses": {
            "Mailing": {
                "City": "New York",
                "StreetLine2": "Apt A",
                "State": "NY",
                "ZipCode": "12345",
                "StreetLine1": "123 Street",
            },
            "Billing": {
                "City": "New York",
                "StreetLine2": "Apt A",
                "State": "NY",
                "ZipCode": "12345",
                "StreetLine1": "123 Street",
            },
        },
        "PhoneNumbers": {"Home": "4448969", "Cell": "0987654321"},
        "LastName": "Cohello",
        "CreatedAt": "2021-11-19",
    }


def test_create_user(user):
    response = client.post(
        "/users/",
        json=user,
    )
    assert response.status_code == 200
    assert response.json() == user


def test_update_user(user):
    update_user = {
        "UID": "45078f7613bf456a8b62497aa3febd83",
        "MiddleName": "Andre",
        "UpdatedAt": "2021-11-19",
        "DOB": "1991-11-19",
        "FirstName": "Carlo",
        "SSN": "123-11-1234",
        "Addresses": {
            "Mailing": {
                "City": "New York",
                "StreetLine2": "Apt A",
                "State": "NY",
                "ZipCode": "12345",
                "StreetLine1": "123 Street",
            },
            "Billing": {
                "City": "New York",
                "StreetLine2": "Apt A",
                "State": "NY",
                "ZipCode": "12345",
                "StreetLine1": "123 Street",
            },
        },
        "PhoneNumbers": {"Home": "4448969", "Cell": "0987654321"},
        "LastName": "Cohello",
        "CreatedAt": "2021-11-21",
    }
    response = client.patch(
        f"/users/{user['UID']}",
        json=update_user,
    )
    assert response.status_code == 200
    assert response.json() == update_user


def test_get_user(user):
    response = client.get(f"/users/{user['UID']}")
    assert response.status_code == 200
    assert response.json() == user
