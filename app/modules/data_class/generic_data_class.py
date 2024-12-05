from flask import request, url_for, redirect, render_template, jsonify, current_app
from typing import Callable, Tuple

from utils import DateUtil
from app.modules.data_class.data_class_base import DataClassBase


class GenericDataClass(DataClassBase):
    def get_method(self):
        pass

    def post_method(self):
        pass

    def put_method(self):
        pass

    def delete_method(self):
        pass
