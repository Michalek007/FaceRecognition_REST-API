from sqlalchemy import Column, Integer, String, Float
from lib_objects import ma
from database import db


class Notifications(db.Model):
    """ Table for notifications.
        Fields -> 'id', 'user_id', 'member_name', 'timestamp'
    """
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    member_name = Column(String, unique=True)
    timestamp = Column(String)


class NotificationsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'member_name', 'timestamp')


notifications_schema = NotificationsSchema()
notifications_many_schema = NotificationsSchema(many=True)
