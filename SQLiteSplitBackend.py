import sqlite3
import uuid
from contextlib import closing
from pprint import pprint


class SQLiteSplitBackend(object):
    def __init__(self):
        self.db = sqlite3.connect('database.db')
        self.db.execute('CREATE TABLE IF NOT EXISTS groups(id TEXT PRIMARY KEY, name TEXT, currency TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS people(id TEXT PRIMARY KEY, name TEXT, group_id TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS '
                        'payments(id TEXT PRIMARY KEY, name TEXT, description TEXT, amount NUMBER, person_id TEXT)')

    async def create_group(self, name, currency) -> uuid:
        group_id = uuid.uuid4()
        with closing(self.db) as conn:
            conn.execute('INSERT INTO groups(id, name, currency) VALUES(?, ?, ?)',
                         (str(group_id), str(name), str(currency)))
            conn.commit()
        return group_id

    async def create_person(self, name, group_id) -> uuid:
        person_id = uuid.uuid4()
        with closing(self.db) as conn:
            conn.execute('INSERT INTO people(id, name, group_id) VALUES(?, ?, ?)',
                         (str(person_id), str(name), str(group_id)))
            conn.commit()
        return person_id

    async def add_payment(self, name, description, amount, person_id) -> uuid:
        payment_id = uuid.uuid4()
        with closing(self.db) as conn:
            conn.execute('INSERT INTO payments(id, name, description, amount, person_id) VALUES(?, ?, ?, ?, ?)',
                         (str(payment_id), str(name), str(description), str(amount), str(person_id)))
            conn.commit()
        return payment_id

    async def get_payments(self, person_id: uuid.UUID | None = None, group_id: uuid.UUID | None = None, payment_id: uuid.UUID | None = None) -> []:
        if person_id is None and group_id is None:
            NotImplemented()

        payments = []

        with closing(self.db) as conn:
            if person_id is not None:
                res = conn.execute('SELECT * FROM payments WHERE person_id = ?', (str(person_id),))
                for payment in res.fetchall():
                    payments.append({'payment_id': uuid.UUID(payment[0]),
                                     'name': payment[1],
                                     'description': payment[2],
                                     'amount': payment[3],
                                     'person_id': uuid.UUID(payment[4])})
            if group_id is not None:
                NotImplemented('TODO: Implement quering payments by group')

            if payment_id is not None:
                NotImplemented('TODO: Implement quering payments by ID')

        return payments
