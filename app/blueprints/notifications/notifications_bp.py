from flask import request, url_for, redirect, render_template, jsonify, current_app
import flask_login
from pyfcm import FCMNotification
from configuration import Config
from datetime import datetime, timedelta
from collections import defaultdict

from app.blueprints import BlueprintSingleton
from database.schemas import Notifications, notifications_many_schema, notifications_schema


class NotificationsBp(BlueprintSingleton):
    """ Implementation of notifications system. """
    client_tokens = []  # Ideally, use a database.
    # fcm = FCMNotification(
    #     service_account_file="secret/facerecognitionapp-3fede-firebase-adminsdk-yd1f9-532abfb0dc.json",
    #     project_id=Config.FCM_PROJECT_ID
    # )
    fcm = None
    notifications = defaultdict(list)

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
        notification_title = "System notification"
        notification_body = "Member name was recognized!"
        result = self.fcm.notify(
            fcm_token=fcm_token,
            notification_title=notification_title,
            notification_body=notification_body,
        )
        return jsonify(result), 200

    def set(self):
        name = request.args.get('name')
        if not name:
            return jsonify(message='Member name must be provided to send notification!'), 404
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify(message='UserID must be provided to send notification!'), 404

        timestamp = datetime.now()
        self.notifications[user_id].append((name, timestamp))
        notification_obj = Notifications(user_id=user_id, member_name=name, timestamp=timestamp)
        db = current_app.config.get('db')
        db.session.add(notification_obj)
        db.session.commit()
        return jsonify(message="Notification added successfully!")

    def get(self):
        user_id = flask_login.current_user.id
        if not self.notifications[user_id]:
            return jsonify(message="No available notifications!")
        name, timestamp = self.notifications[user_id].pop(0)
        if name == 'unknown':
            message = f"Unknown person detected at {timestamp}!"
        else:
            message = f"Member {name} recognized at {timestamp}!"
        return jsonify(message=message)

    def get_all(self):
        return jsonify(notifications_many_schema.dump(Notifications.query.all()))

    # gui views
    def fcm_view(self):
        return render_template('notifications/fcm.html')

    def table(self):
        return render_template('notifications/notifications_table.html')
