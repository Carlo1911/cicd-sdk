import json
from pathlib import Path
from typing import Union

import pytest


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def _load_fixture_from_file(file_name: Union[str, Path]) -> dict:
    path = str(FIXTURES_DIR / file_name)
    with open(path) as file:
        return json.loads(file.read())


@pytest.fixture
def user():
    return _load_fixture_from_file("user.json")


@pytest.fixture
def user_minimal():
    return _load_fixture_from_file("user_minimal.json")


@pytest.fixture
def user_with_updates():
    return _load_fixture_from_file("user_with_updates.json")


@pytest.fixture
def user_minimal_with_updates():
    return _load_fixture_from_file("user_minimal_with_updates.json")


@pytest.fixture
def user_with_wrong_date_format():
    return _load_fixture_from_file("user_with_wrong_date_format.json")


@pytest.fixture
def user_with_wrong_social_security_number():
    return _load_fixture_from_file("user_with_wrong_social_security_number.json")


@pytest.fixture
def user_with_extra_field():
    return _load_fixture_from_file("user_with_extra_field.json")
