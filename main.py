from fastapi import FastAPI

from SQLiteSplitBackend import SQLiteSplitBackend
from OpenSplitterTypes import *

app = FastAPI()
split_backend = SQLiteSplitBackend()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/group/create')
async def create_group(body: CreateGroupBody):
    group_id = await split_backend.create_group(body.name, body.currency)
    return {'status': 'OK', 'uuid': group_id}


@app.get('/group/query')
async def query_group(group_uuid: uuid.UUID):
    group: Group | None = await split_backend.get_group(group_uuid)
    return {'status': 'OK', 'group': group}


@app.post('/person/create')
async def create_person(body: CreatePersonBody):
    person_id = await split_backend.create_person(body.name, body.group_uuid),
    return {'status': 'OK', 'uuid': person_id}


@app.post('/payments/add')
async def add_payment(body: AddPaymentBody):
    payment_id = await split_backend.add_payment(body.name, body.description, body.amount, body.person_uuid)
    return {'status': 'OK', 'uuid': payment_id}


@app.get('/payments/query')
async def query_payments(person_uuid: uuid.UUID | None = None,
                         group_uuid: uuid.UUID | None = None,
                         payment_uuid: uuid.UUID | None = None):
    payments = await split_backend.get_payments(person_uuid, group_uuid, payment_uuid)
    return {'status': 'OK', 'payments': payments}
