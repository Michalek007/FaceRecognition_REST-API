from flask import request, jsonify, render_template, current_app

from app.blueprints import BlueprintSingleton
from configuration import Config


class DetailsBp(BlueprintSingleton):
    """ Implements views related to service detailed info."""

    @staticmethod
    def get_service_methods():
        from app.blueprints.auth.views import login
        from app.blueprints.user.views import register, logout, protected, users
        from app.blueprints.details.views import app_details
        return [
            login,
            logout,
            protected,
            register,
            users,
            app_details,
        ]

    # private methods
    # views
    def app_details(self):
        data = Config.get_project_details()
        return jsonify(ProjectName=data.metadata.PROJECT_NAME,
                       Version=data.metadata.VERSION,
                       RootDirectory=current_app.config.get('BASEDIR'),
                       HostName=current_app.config.get('COMPUTER_NAME'))

    def help(self, method=None):
        def format_doc(function):
            if function.__doc__ is None:
                return ""
            doc = list(map(lambda x: x.lstrip(), function.__doc__.split('\n')))
            if doc[-1] == "":
                doc.pop()
            return " ".join(doc)

        methods = self.get_service_methods()
        api_methods = {method.__name__: format_doc(method) for method in methods}
        if not method:
            return jsonify(api_methods=api_methods)
        try:
            documentation = api_methods[method]
        except KeyError:
            return jsonify(message='There is no method in api with that name.'), 404
        return jsonify({method: documentation})

    # gui views
    def info(self):
        return render_template('details/details.html')

    def methods(self):
        return render_template('details/methods.html')
