from abc import ABC, abstractmethod
from typing import Callable, Tuple


class DataClassBase(ABC):
    """ Abstract base data class. """
    def __init__(self, data_name, data_table_class, data_ma_schema, data_ma_many_schema,
                 get_data_from_request: Tuple[Callable, str], create_data_obj: Callable, set_data_obj_values: Callable):
        self.data_name = data_name
        self.data_table_class = data_table_class
        self.data_ma_schema = data_ma_schema
        self.data_ma_many_schema = data_ma_many_schema

        self.get_data_from_request = get_data_from_request
        self.create_data_obj = create_data_obj
        self.set_data_obj_values = set_data_obj_values

    @abstractmethod
    def get_method(self):
        pass

    @abstractmethod
    def post_method(self):
        pass

    @abstractmethod
    def put_method(self):
        pass

    @abstractmethod
    def delete_method(self):
        pass
