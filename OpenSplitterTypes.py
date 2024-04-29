import uuid

from pydantic import BaseModel


class Payment(BaseModel):
    payment_uuid: uuid.UUID
    name: str
    description: str | None = None
    amount: float
    person_uuid: uuid.UUID


class Group(BaseModel):
    group_uuid: uuid.UUID
    name: str
    currency: str


# Base data models for API requests
class CreateGroupBody(BaseModel):
    name: str
    currency: str


class CreatePersonBody(BaseModel):
    name: str
    group_uuid: uuid.UUID


class AddPaymentBody(BaseModel):
    name: str
    description: str | None = None
    amount: float
    person_uuid: uuid.UUID
