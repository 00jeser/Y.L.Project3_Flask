import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

class Car(SqlAlchemyBase):
    __tablename__ = 'cars'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    maxSpeed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    to100 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    createdDate = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    addedInGameDls = sqlalchemy.Column(sqlalchemy.String)
