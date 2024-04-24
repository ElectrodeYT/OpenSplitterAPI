import uuid
from fastapi import FastAPI
from pydantic import BaseModel

from SQLiteSplitBackend import SQLiteSplitBackend

app = FastAPI()
split_backend = SQLiteSplitBackend()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


class CreateGroupBody(BaseModel):
    name: str
    currency: str


@app.post('/group/create')
async def create_group(body: CreateGroupBody):
    group_id = await split_backend.create_group(body.name, body.currency)
    return {'status': 'OK', 'message': 'Group created successfully', 'uuid': group_id}


class CreatePersonBody(BaseModel):
    name: str
    group_uuid: uuid.UUID


@app.post('/person/create')
async def create_person(body: CreatePersonBody):
    person_id = await split_backend.create_person(body.name, body.group_uuid),
    return {'status': 'OK', 'message': 'Person created successfully', 'uuid': person_id}


class PaymentBody(BaseModel):
    name: str
    description: str | None = None
    amount: float
    person_uuid: uuid.UUID


@app.post('/payments/add')
async def add_payment(body: PaymentBody):
    payment_id = await split_backend.add_payment(body.name, body.description, body.amount, body.person_uuid)
    return {'status': 'OK', 'message': 'Payment added', 'uuid': payment_id}


@app.get('/payments/query')
async def query_payments(person_uuid: uuid.UUID | None = None, group_uuid: uuid.UUID | None = None):
    payments = await split_backend.get_payments(person_uuid, group_uuid)
    return {'status': 'OK', 'message': 'Payments queried', 'payments': payments}