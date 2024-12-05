""" Contains modules with library objects, which behaves as singleton implementation.
    Purpose of this package was to handle circular import error in case these objects
    were used in different parts of project than app.
"""
from lib_objects.bcrypt import bcrypt
from lib_objects.ma import ma
