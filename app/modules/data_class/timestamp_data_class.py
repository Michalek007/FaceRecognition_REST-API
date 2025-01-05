from flask import request, url_for, redirect, render_template, jsonify, current_app
from typing import Callable, Tuple

from utils import DateUtil
from app.modules.data_class.data_class_base import DataClassBase


class TimestampDataClass(DataClassBase):
    """ Data class for database tables with timestamp column.
        Implements CRUD functionalities based on timestamp input.
    """
    def __init__(self, data_name, data_table_class, data_ma_schema, data_ma_many_schema,
                 get_data_from_request: Tuple[Callable, str], create_data_obj: Callable, set_data_obj_values: Callable):
        super().__init__(data_name, data_table_class, data_ma_schema, data_ma_many_schema,
                         get_data_from_request, create_data_obj, set_data_obj_values)

        self.date_util = DateUtil(['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'])

    def get_method(self, obj_id: int = None):
        """ HTTP GET method implementation.
            Returns data object with given id if given, or list of data objects later than given timestamp.
            If no input given, returns list of all data objects.
        """
        if obj_id is None:
            # # # getting objects based on timestamp
            timestamp = request.args.get('timestamp')
            data_obj = self.data_table_class.query.all()
            if timestamp is None:
                return jsonify(output=self.data_ma_many_schema.dump(data_obj))

            timestamp = self.date_util.from_string(timestamp)
            if timestamp is None:
                return jsonify(message='Wrong date format. Expected: %Y-%m-%d %H:%M:%S or %Y-%m-%d')

            later_obj = filter(
                lambda item: self.date_util.from_string(item.timestamp) > timestamp, data_obj
            )
            return jsonify(output=self.data_ma_many_schema.dump(later_obj))

        # # # getting object based on id
        data_obj = self.data_table_class.query.filter_by(id=obj_id).first()
        if data_obj:
            return jsonify(output=self.data_ma_schema.dump(data_obj))
        else:
            return jsonify(message=f'There are no {self.data_name} with that id'), 404

    def delete_method(self, obj_id: int = None):
        """ HTTP DELETE method implementation.
            Deletes data object with given id if given, or data objects earlier than given timestamp.
        """
        if obj_id is None:

            # # # getting and validating timestamp
            timestamp = request.args.get('timestamp')
            if timestamp is None:
                return jsonify(message='Missing value. Expected arg: Timestamp'), 400

            timestamp = self.date_util.from_string(timestamp)
            if timestamp is None:
                return jsonify(message='Wrong date format. Expected: %Y-%m-%d %H:%M:%S or %Y-%m-%d')

            # # # deleting object based on timestamp
            data_obj = self.data_table_class.query.all()
            earlier_obj = filter(
                lambda item: self.date_util.from_string(item.timestamp) < timestamp, data_obj
            )
            earlier_obj = list(earlier_obj)
            for param in earlier_obj:
                current_app.config.get('db').session.delete(param)
            current_app.config.get('db').session.commit()

            deleted_count = len(earlier_obj)
            if deleted_count == 0:
                return jsonify(message=f'No {self.data_name} were deleted. '), 404
            return jsonify(message=f'{deleted_count} {self.data_name} deleted successfully'), 202

        # # # deleting object based on id
        data_obj = self.data_table_class.query.filter_by(id=obj_id).first()
        if data_obj:
            current_app.config.get('db').session.delete(data_obj)
            current_app.config.get('db').session.commit()
            return jsonify(message=f'Deleted {self.data_name} from ' + data_obj.timestamp), 202
        else:
            return jsonify(message=f'There are no {self.data_name} with that id'), 404

    def post_method(self):
        """ HTTP POST method implementation.
            Adds data object in database with given input data + timestamp.
        """
        # # # collecting data
        response = self.get_data_from_request[0]()
        if not response:
            return jsonify(message=self.get_data_from_request[1]), 400
        else:
            collected_data = response

        # # # creating & adding object in database
        data_obj = self.create_data_obj(collected_data)
        current_app.config.get('db').session.add(data_obj)
        current_app.config.get('db').session.commit()
        return jsonify(message=f'Added new {self.data_name} from ' + data_obj.timestamp), 202

    def put_method(self, obj_id: int = None):
        """ HTTP PUT method implementation.
            Updates data object values in database with given input data.
        """
        if obj_id is None:
            return jsonify(message=f'There is no {self.data_name} with that id'), 404

        # # # collecting data
        response = self.get_data_from_request[0]()
        if not response:
            return jsonify(message=self.get_data_from_request[1]), 400
        else:
            collected_data = response

        # # # searching for object with given id & updating values
        data_obj = self.data_table_class.query.filter_by(id=obj_id).first()
        if data_obj:
            self.set_data_obj_values(data_obj, collected_data)
            current_app.config.get('db').session.commit()
            return jsonify(message=f'Updated {self.data_name} from ' + data_obj.timestamp), 202
        else:
            return jsonify(message=f'There are no {self.data_name} with that id'), 404
