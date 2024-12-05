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
        from app.blueprints.acc.views import acc, add_acc, delete_acc, update_acc
        from app.blueprints.controls.views import get_action, update_action
        from app.blueprints.env_metrics.views import env_metrics, add_env_metrics, update_env_metrics, delete_env_metrics
        return [
            login,
            logout,
            protected,
            register,
            users,
            app_details,
            acc,
            add_acc,
            delete_acc,
            update_acc,
            get_action,
            update_action,
            env_metrics,
            add_env_metrics,
            update_env_metrics,
            delete_env_metrics
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
