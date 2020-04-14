import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from json import JSONEncoder


class Car(SqlAlchemyBase, JSONEncoder):
    __tablename__ = 'cars'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    maxSpeed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    mass = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    persons = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    engineType = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    buyPryce = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    sellPryce = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    mil14 = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    mil12 = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    mil1 = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    control = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    stop = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    clas = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    privod = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    addedInGameDlS = sqlalchemy.Column(sqlalchemy.String)
    def default(self, o):
            return o.__dict__

