from flask import request, jsonify, render_template, current_app

from app.blueprints import BlueprintSingleton
from utils import SubprocessApi, ProcessUtil
from configuration import Pid


class ConfigBp(BlueprintSingleton):
    """ Implements views related to service configuration.
        Attributes:
            subprocess: SubprocessApi instance
            process_util: ProcessUtil instance
    """
    subprocess = SubprocessApi()
    process_util = ProcessUtil()

    # private methods
    def kill_service(self):
        self.process_util.task_kill(pid=Pid.SERVICE)

    # views
    def get_pid(self):
        return jsonify(service=Pid.SERVICE)

    def kill(self):
        self.kill_service()
        return jsonify(message='Service is shut down!')

    def restart(self):
        self.kill_service()
        restart_script = current_app.config.get("RESTART_SCRIPT")
        run_file = current_app.config.get("RUN_FILE")
        self.subprocess.run(f'start {restart_script} {run_file}', stdout=None, stderr=None)
        return jsonify(message='Service is restarting!')

    # gui views
    def settings(self):
        return render_template('config/settings.html')
