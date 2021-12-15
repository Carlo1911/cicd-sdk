from datetime import date

import boto3
from pydantic import BaseModel


class Address(BaseModel):
    """Model to represent an address

    :param BaseModel: Class to represent a data model
    :type BaseModel: class:`pydantic.BaseModel`

    :param StreetLine1: Street address line 1
    :param StreetLine1: str
    :param StreetLine2: Street address line 2
    :param StreetLine2: str
    """

    StreetLine1: str
    StreetLine2: str
    City: str
    State: str
    ZipCode: str


class User(BaseModel):
    """Data model for a user.

        :param BaseModel: Class to represent a data model
        :type BaseModel: class:`pydantic.BaseModel`

        :param UID: Unique identifier for the user
        :type UID: str
        :param DOB: Date of birth
        :type DOB: datetime.date


        Example:
            {
        "UID": "123456789",
        "FirstName": "Carlo",
        "MiddleName": "Andre",
        "LastName": "Alva",
        "DOB": "1991-11-19",
        "Addresses": {
            "Mailing": {
                "StreetLine1": "123 Street",
                "StreetLine2": "Apt A",
                "City": "New York",
                "State": "NY",
                "ZipCode": "12345"
            },
            "Billing": {
                "StreetLine1": "123 Street",
                "StreetLine2": "Apt A",
                "City": "New York",
                "State": "NY",
                "ZipCode": "12345"
            }
        },
        "PhoneNumbers": {
            "Home": "1234567890",
            "Cell": "0987654321"
        },
        "SSN": "123-11-1234",
        "CreatedAt": "2021-11-19",
        "UpdatedAt": "2021-11-19"
    }

    """

    UID: str
    FirstName: str
    MiddleName: str
    LastName: str
    DOB: date  # TODO: Check iso8601
    Addresses: dict[str, Address]
    PhoneNumbers: dict[str, str]
    SSN: str
    CreatedAt: date  # TODO: Check iso8601
    UpdatedAt: date  # TODO: Check iso8601

    @property
    def to_mongo(self):
        serializer = boto3.dynamodb.types.TypeSerializer()
        ow_level_copy = {k: serializer.serialize(v) for k, v in self.dict().items()}
        return ow_level_copy
