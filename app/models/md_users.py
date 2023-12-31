from sqlalchemy import Column, String, Integer, ForeignKey
from app.db.connection import db


class Users(db.Model):
    username = Column(String(50), primary_key=True)
    email = Column(String(1000), unique=True)
    passwd = Column(String(10000))
    rol = Column(String(30))
    id_teacher = Column(Integer, ForeignKey("teacher.id"))

    def to_json(self):
        return {
            "username": self.username,
            "email": self.email,
            "rol": self.rol,
            "id_teacher": self.id_teacher
        }

    def __init__(self, username, email, passwd, rol, id_teacher=None) -> None:
        self.username = username
        self.email = email
        self.passwd = passwd
        self.rol = rol
        self.id_teacher = id_teacher
