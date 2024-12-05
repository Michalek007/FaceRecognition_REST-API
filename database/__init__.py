""" Contains SQAlchemy database object, models & schemas. """
from flask_sqlalchemy import SQLAlchemy


def create_db_object():
    """ Returns database SQLAlchemy object. """
    sql_alchemy = SQLAlchemy()
    return sql_alchemy


db = SQLAlchemy()
