import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator
from src.core.utils import to_camel
from typing_extensions import Annotated


class Address(BaseModel):
    """Model to represent an address

    :param BaseModel: Class to represent a data model
    :type BaseModel: class:`pydantic.BaseModel`

    :param street_line_1: Street address line 1
    :param street_line_1: str
    :param street_line_2: Street address line 2
    :param street_line_2: str
    :param city: Name of the city
    :param city: str
    :param state: Name of the state
    :param state: str
    :param zip_code: Zip code
    :param zip_code: str
    """

    street_line_1: str
    street_line_2: Optional[str]
    city: str
    state: str
    zip_code: str

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        extra = "forbid"


class User(BaseModel):
    """Data model for a user.

        :param BaseModel: Class to represent a data model
        :type BaseModel: class:`pydantic.BaseModel`

        :param uid: Unique identifier for the user
        :type uid: str
        :param dob: Date of birth
        :type dob: datetime.date
        :param last4Ssn: Last four Social Security Number
        :type last4Ssn: str

        Example:
            {
        "uid": "123456789",
        "firstName": "Carlo",
        "middleName": "Andre",
        "lastName": "Alva",
        "dob": "1991-11-19",
        "addresses": {
            "mailing": {
                "streetLine1": "123 Street",
                "streetLine2": "Apt A",
                "city": "New York",
                "state": "NY",
                "zipCode": "12345"
            },
            "billing": {
                "streetLine1": "123 Street",
                "streetLine2": "Apt A",
                "city": "New York",
                "state": "NY",
                "zipCode": "12345"
            }
        },
        "phoneNumbers": {
            "home": "1234567890",
            "cell": "0987654321"
        },
        "last4Ssn": "1234",
        "createdAt": "2021-11-19",
        "updatedAt": "2021-11-19"
    }

    """

    uid: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    first_name: str
    middle_name: Optional[str]
    last_name: str
    date_of_birth: str = Field(alias="dob")
    addresses: dict[str, Address]
    phone_numbers: dict[str, str]
    last_4_social_security_number: str = Field(alias="last4Ssn", max_length=4)
    created_at: str
    updated_at: str

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        extra = "forbid"

    @validator("date_of_birth", "created_at", "updated_at")
    def check_date_format(cls, value):
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return value
