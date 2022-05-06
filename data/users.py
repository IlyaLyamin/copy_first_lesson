import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, name="фамилия")
    name = sqlalchemy.Column(sqlalchemy.String, name="имя")
    age = sqlalchemy.Column(sqlalchemy.Integer, name="возраст")
    position = sqlalchemy.Column(sqlalchemy.String, name="должность")
    speciality = sqlalchemy.Column(sqlalchemy.String, name="профессия")
    address = sqlalchemy.Column(sqlalchemy.String, name="адрес")
    email = sqlalchemy.Column(sqlalchemy.String, name="электронная почта", unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, default="123123", name="хэшированый пароль")
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now(), name="дата изменения")
    photo = sqlalchemy.Column(sqlalchemy.String)
    jobs = orm.relation("Jobs", back_populates='user')

    def __repr__(self):
        return f" <Colonist> {self.id} {self.surname} {self.name}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)