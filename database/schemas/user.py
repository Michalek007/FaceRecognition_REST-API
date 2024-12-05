from sqlalchemy import Column, Integer, String
from database import db
from lib_objects import ma


class User(db.Model):
    """ Table for service users.
        Fields -> 'id', 'username', 'pw_hash'
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    pw_hash = Column(String)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'pw_hash')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
