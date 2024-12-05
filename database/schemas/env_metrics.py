from sqlalchemy import Column, Integer, String, Float
from lib_objects import ma
from database import db


class EnvMetrics(db.Model):
    """ Table for environmental metrics (temperature, pressure, humidity).
        Fields -> 'id', 'timestamp', 'temperature', 'pressure', 'humidity'
    """
    __tablename__ = 'env_metrics'
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)


class EnvMetricsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'timestamp', 'temperature', 'pressure', 'humidity')


env_metrics_schema = EnvMetricsSchema()
env_metrics_many_schema = EnvMetricsSchema(many=True)
