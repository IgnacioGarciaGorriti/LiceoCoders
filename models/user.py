import uuid

from flask_login import UserMixin
from sqlalchemy import Column, String, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from models.base import Base


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(String(255), primary_key=True)
    username = Column(String(255))
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    age = Column(Integer)
    gender = Column(String(255))
    role = Column(String(255))
    points = Column(Integer)
    status = Column(String(255))

    def __init__(self, username, name, surname, email, password, age, gender, role, points=0, status='Beginner', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = str(uuid.uuid4())
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email
        self.password = generate_password_hash(password)
        self.age = age
        self.gender = gender
        self.role = role
        self.points = points
        self.status = status

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self, type: str = 'obj'):
        if type == 'show':
            return {
                'id': self.id,
                'username': self.username,
                'name': self.name,
                'surname': self.surname,
                'email': self.email,
                'age': self.age,
                'gender': self.gender,
                'role': self.role,
                'points': self.points,
                'status': self.status,
            }
        elif type == 'list':
            return {
                'id': self.id,
                'username': self.username,
            }
        elif type == 'obj':
            return {
                'id': self.id,
                'username': self.username,
                'name': self.name,
                'surname': self.surname,
                'email': self.email,
                'password': self.password,
                'age': self.age,
                'gender': self.gender,
                'role': self.role,
                'points': self.points,
                'status': self.status,
            }
