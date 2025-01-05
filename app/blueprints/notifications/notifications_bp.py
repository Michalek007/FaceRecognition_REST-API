from flask import request, url_for, redirect, render_template, jsonify, current_app
import flask_login
from pyfcm import FCMNotification
from configuration import Config

from app.blueprints import BlueprintSingleton



class NotificationsBp(BlueprintSingleton):
    """ Implementation of notifications system. """
    client_tokens = []  # Ideally, use a database.
    fcm = FCMNotification(
        service_account_file="secret/facerecognitionapp-3fede-firebase-adminsdk-yd1f9-532abfb0dc.json",
        project_id=Config.FCM_PROJECT_ID
    )

    def register_token(self):
        token = request.form.get('token')
        if token not in self.client_tokens:
            self.client_tokens.append(token)
        return jsonify({"message": "Token registered successfully."}), 200

    def send(self):
        # title = request.form.get('title')
        # body = request.form.get('body')
        # client_id = request.form.get('body')
        # fcm_token = "<fcm token>"
        fcm_token = self.client_tokens[0]
        notification_title = "Uber update"
        notification_body = "Hi John, your order is on the way!"
        # notification_image = "https://example.com/image.png"
        result = self.fcm.notify(
            fcm_token=fcm_token,
            notification_title=notification_title,
            notification_body=notification_body,
            # notification_image=notification_image
        )
        return jsonify(result), 200

    # gui views
    def fcm_view(self):
        return render_template('notifications/fcm.html')
