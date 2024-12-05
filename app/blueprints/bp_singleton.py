
class BlueprintSingleton:
    """ Base class for all blueprints classes.
        Implements singleton pattern.
    """
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance


### blueprint class schema
# from flask import request, jsonify, render_template, current_app
#
# from app.blueprints import BlueprintSingleton
# from app.blueprints.blueprint.modules import Module
#
#
# class ClassBp(BlueprintSingleton):
#     """ Implements methods related to something.
#     """
#     # class attributes
#     # private methods
#     # views
#     # gui views
#     pass
