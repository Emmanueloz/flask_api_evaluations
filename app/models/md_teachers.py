from sqlalchemy import Column, String, Integer
from app.db.connection import db
import random


class Teacher(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    subject = Column(String(100))

    def random_id():
        return random.randint(1, 99999)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "subject": self.subject
        }

    def __init__(self, name, subject, id=None):
        self.id = id if id is not None else self.random_id()
        self.name = name
        self.subject = subject
