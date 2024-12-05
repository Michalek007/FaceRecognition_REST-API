from flask import request, url_for, redirect, render_template, jsonify, current_app
from datetime import datetime

from app.blueprints import BlueprintSingleton
from database.schemas import env_metrics_schema, env_metrics_many_schema, EnvMetrics
from utils import DateUtil
from app.modules.data_class import TimestampDataClass


class EnvMetricsBp(BlueprintSingleton):
    """ Implementation of CRUD functionalities for environmental metrics data (env metrics table).
        Attributes:
            date_util: DateUtil object
            env_metrics_clas: TimestampDataClass object
    """
    date_util = DateUtil(
        date_format='%Y-%m-%d %H:%M:%S.%f',
        optional_date_format=('%Y-%m-%d %H:%M:%S', '%Y-%m-%d')
    )

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            cls._instance.env_metrics_class = TimestampDataClass(data_name='env metrics',
                                                                 data_table_class=EnvMetrics,
                                                                 data_ma_schema=env_metrics_schema,
                                                                 data_ma_many_schema=env_metrics_many_schema,
                                                                 get_data_from_request=(
                                                                    cls.get_env_metrics_data_from_request,
                                                                    'Missing value. Expected args: Temperature, Pressure, Humidity'
                                                                 ),
                                                                 create_data_obj=cls.create_env_metrics_obj,
                                                                 set_data_obj_values=cls.set_env_metrics_obj_values)
        return cls._instance

    @staticmethod
    def get_env_metrics_data_from_request():
        temperature = request.args.get('Temperature')
        pressure = request.args.get('Pressure')
        humidity = request.args.get('Humidity')
        if temperature is None or pressure is None or humidity is None:
            return None
        else:
            return temperature, pressure, humidity

    @staticmethod
    def create_env_metrics_obj(data):
        timestamp = datetime.now()
        env_metrics_obj = EnvMetrics(
            timestamp=timestamp,
            temperature=data[0],
            pressure=data[1],
            humidity=data[2]
        )
        return env_metrics_obj

    @staticmethod
    def set_env_metrics_obj_values(env_metrics_obj, data):
        env_metrics_obj.temperature = data[0]
        env_metrics_obj.pressure = data[1]
        env_metrics_obj.humidity = data[2]
        return env_metrics_obj

    # views
    def env_metrics(self, env_metrics_id: int = None):
        return self.env_metrics_class.get_method(obj_id=env_metrics_id)

    def add_env_metrics(self):
        return self.env_metrics_class.post_method()

    def delete_env_metrics(self, env_metrics_id: int = None):
        return self.env_metrics_class.delete_method(obj_id=env_metrics_id)

    def update_env_metrics(self, env_metrics_id: int = None):
        return self.env_metrics_class.put_method(obj_id=env_metrics_id)

    # gui views
    def env_metrics_table(self):
        return render_template('env_metrics/env_metrics_table.html')
