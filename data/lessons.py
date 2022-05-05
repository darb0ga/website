import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lesson'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    place = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("subject.id"))
    subject = orm.relation('Subject')
