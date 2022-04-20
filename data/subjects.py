import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Subject(SqlAlchemyBase):
    __tablename__ = 'subject'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_hard = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id")
    user = orm.relation('User')
