from flask import request, url_for, redirect, render_template, jsonify, current_app
from datetime import datetime

from app.blueprints import BlueprintSingleton
from database.schemas import acceleration_schema, acceleration_many_schema, Acceleration
from utils import DateUtil
from app.modules.data_class import TimestampDataClass


class AccBp(BlueprintSingleton):
    """ Implementation of CRUD functionalities for acc (acceleration table).
        Attributes:
            date_util: DateUtil object
            acc_clas: TimestampDataClass object
    """
    date_util = DateUtil(
        date_format='%Y-%m-%d %H:%M:%S.%f',
        optional_date_format=('%Y-%m-%d %H:%M:%S', '%Y-%m-%d')
    )

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            cls._instance.acc_clas = TimestampDataClass(data_name='acc',
                                                        data_table_class=Acceleration,
                                                        data_ma_schema=acceleration_schema,
                                                        data_ma_many_schema=acceleration_many_schema,
                                                        get_data_from_request=(
                                                            cls.get_acc_data_from_request,
                                                            'Missing value. Expected args: X, Y, Z'
                                                        ),
                                                        create_data_obj=cls.create_acc_obj,
                                                        set_data_obj_values=cls.set_acc_obj_values)
        return cls._instance

    @staticmethod
    def get_acc_data_from_request():
        x_axis = request.args.get('X')
        y_axis = request.args.get('Y')
        z_axis = request.args.get('Z')
        if x_axis is None or y_axis is None or z_axis is None:
            return None
        else:
            return x_axis, y_axis, z_axis

    @staticmethod
    def create_acc_obj(data):
        timestamp = datetime.now()
        acc_obj = Acceleration(
            timestamp=timestamp,
            x_axis=data[0],
            y_axis=data[1],
            z_axis=data[2]
        )
        return acc_obj

    @staticmethod
    def set_acc_obj_values(acc_obj, data):
        acc_obj.x_axis = data[0]
        acc_obj.y_axis = data[1]
        acc_obj.z_axis = data[2]
        return acc_obj

    # views
    def acc(self, acc_id: int = None):
        return self.acc_clas.get_method(obj_id=acc_id)

    def add_acc(self):
        return self.acc_clas.post_method()

    def delete_acc(self, acc_id: int = None):
        return self.acc_clas.delete_method(obj_id=acc_id)

    def update_acc(self, acc_id: int = None):
        return self.acc_clas.put_method(obj_id=acc_id)

    # gui views
    def acc_table(self):
        return render_template('acc/acc_table.html')
