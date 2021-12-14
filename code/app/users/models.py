from datetime import datetime

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
        "FirstName": "First",
        "MiddleName": "Middle"
        "LastName": "Last",
        "DOB": YYYY-MM-DD (ISO 8601),
        "Addresses": {
           "Mailing": {
           "StreetLine1": "123 Street",
           "StreetLine2": "Apt A",
           "City": "New York",
           "State": "NY",
           "ZipCode": "12345",
        },
        "Billing": {
          "StreetLine1": "123 Street",
         "StreetLine2": "Apt A",
         "City": "New York",
         "State": "NY",
         "ZipCode": "12345",
         },
        },
         "PhoneNumbers": {
          "Home": "1234567890",
          "Cell": "0987654321",
          },
          "SSN": "XXX-XX-1234",
          "CreatedAt": YYYY-MM-DD (ISO 8601),
         "UpdatedAt": YYYY-MM-DD (ISO 8601),
        }

    :param collector_id: The collector ID
    :return: (reviews aggregates, iterable of reviews)
    """

    UID: str
    FirstName: str
    MiddleName: str
    LastName: str
    DOB: datetime  # TODO: Check iso8601
    Addresses: dict
    Billing: Address
    PhoneNumbers: dict
    SSN: str
    CreatedAt: datetime  # TODO: Check iso8601
    UpdatedAt: datetime  # TODO: Check iso8601
