from sqlalchemy import Column, Integer, String, Float
from lib_objects import ma
from database import db


class Members(db.Model):
    """ Table for members.
        Fields -> 'id', 'user_id', 'name', 'embedding', 'image'
    """
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String)
    embedding = Column(String)
    image = Column(String)


class MembersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'name', 'embedding', 'image')


members_schema = MembersSchema()
members_many_schema = MembersSchema(many=True)
