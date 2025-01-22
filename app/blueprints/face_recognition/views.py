import flask_login

from app.blueprints.face_recognition import face_recognition as face_recognition_bp
from app.blueprints.face_recognition.face_recognition_bp import FaceRecognitionBp


@face_recognition_bp.route("/recognize/", methods=['POST'])
@flask_login.login_required
def recognize():
    return FaceRecognitionBp().recognize()
