from flask import request, url_for, redirect, render_template, jsonify, current_app
import flask_login
import os
import shutil
from PIL import Image, ImageDraw
import torch
import requests
from pathlib import Path

from app.blueprints import BlueprintSingleton
from database.schemas import members_schema, members_many_schema, Members
from app.modules.face_recognition import mtcnn, resnet


class MembersBp(BlueprintSingleton):
    """ Implementation of CRUD functionalities for members table.
        Attributes:
            mtcnn: MTCNN model
            resnet: InceptionResnetV1 model
    """
    mtcnn = mtcnn
    resnet = resnet

    @staticmethod
    def create_members_obj(data):
        members_obj = Members(
            user_id=data[0],
            name=data[1],
            embedding=data[2],
            image=data[3]
        )
        return members_obj

    # views
    def get(self, members_id: int = None):
        return {}

    def add(self):
        return {}

    def delete(self, members_id: int = None):
        return {}

    def update(self, members_id: int = None):
        return {}

    def upload_image(self):
        try:
            filename = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), 'temp_member.jpg')
            request.files.get('file').save(filename)
        except AttributeError:
            return jsonify(message=f'File not found in request body!'), 404

        image = Image.open(filename)
        boxes, _ = self.mtcnn.detect(image)
        draw = ImageDraw.Draw(image)
        for box in boxes:
            draw.rectangle(box.tolist(), outline='red', width=3)
        filename = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), 'temp_member_detected.jpg')
        image.save(filename)
        image_url = f'http://{current_app.config.get("LISTENER").get("host")}:{current_app.config.get("LISTENER").get("port")}/static/temp/temp_member_detected.jpg'
        return render_template("members/add.html", member_image=image_url)

    def new(self):
        name = request.form.get('name')
        if not name:
            return jsonify(message='New member name was not provided!'), 404
        user_id = flask_login.current_user.id
        # check if name not already exist for  user members

        filename = name.replace(' ', '')
        image = os.path.join(current_app.config.get('IMAGES_DIR'), filename+'.jpg')
        temp_image = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), 'temp_member.jpg')
        shutil.copy(temp_image, image)
        embedding_file = os.path.join(current_app.config.get('EMBEDDINGS_DIR'), filename+'.pt')

        img = Image.open(image)
        aligned = self.mtcnn(img).unsqueeze(0)
        embeddings = self.resnet(aligned).detach()[0]
        torch.save(embeddings, embedding_file)

        # response = requests.post(url_for('members.add'))
        db = current_app.config.get('db')
        members_obj = self.create_members_obj((user_id, name, embedding_file, image))
        db.session.add(members_obj)
        db.session.commit()

        Path(temp_image).unlink(missing_ok=True)
        Path(current_app.config.get('TEMP_UPLOAD_DIR'), 'temp_member_detected.jpg').unlink(missing_ok=True)

        return jsonify(message='New member added!')

    # gui views
    def table(self):
        return render_template('members/members_table.html')

    def upload(self):
        return render_template('members/upload.html')
