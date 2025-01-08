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
from app.modules.face_recognition import mtcnn, resnet, lite_face


class MembersBp(BlueprintSingleton):
    """ Implementation of CRUD functionalities for members table.
        Attributes:
            mtcnn: MTCNN model
            resnet: InceptionResnetV1 model
            lite_face: LiteFace model
    """
    mtcnn = mtcnn
    resnet = resnet
    lite_face = lite_face

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
    def get(self, member_id: int = None):
        if member_id is None:
            user_id = request.args.get("user_id")
            if user_id is None:
                return jsonify(members_many_schema.dump(Members.query.all()))

            members_list = Members.query.filter_by(user_id=user_id).all()
            if not members_list:
                return jsonify(message=f'There are no members with given user_id'), 404
            return jsonify(members_many_schema.dump(members_list))

        members_obj = Members.query.filter_by(id=member_id).first()
        if members_obj:
            return jsonify(members_schema.dump(members_obj))
        else:
            return jsonify(message=f'There is no member with given id'), 404

    def add(self):
        return {}

    def delete(self):
        user_id = flask_login.current_user.id
        name = request.args.get('name')
        if not name:
            return jsonify(message=f'Member name was not provided.'), 404
        members_obj = Members.query.filter_by(user_id=user_id, name=name).first()
        if not members_obj:
            return jsonify(message=f'There is no member with given name.'), 404
        try:
            Path(members_obj.embedding+'.pt').unlink(missing_ok=True)
            Path(members_obj.image+'.jpg').unlink(missing_ok=True)
            shutil.rmtree(members_obj.embedding, ignore_errors=False)
            shutil.rmtree(members_obj.image, ignore_errors=False)
        except PermissionError:
            return jsonify(message=f'Member cannot be deleted when system is working.')
        db = current_app.config.get('db')
        db.session.delete(members_obj)
        db.session.commit()
        return jsonify(message=f'Member {name} deleted successfully.')

    def update(self, member_id: int = None):
        return {}

    def upload_image(self):
        user_id = flask_login.current_user.id
        image_id = f'temp_member_{user_id}'
        try:
            filename = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), f'{image_id}.jpg')
            request.files.get('file').save(filename)
        except AttributeError:
            return jsonify(message=f'File not found in request body!'), 404

        base_url = f'http://{current_app.config.get("LISTENER").get("host")}:{current_app.config.get("LISTENER").get("port")}/static/temp'
        image_url = f'{base_url}/{image_id}.jpg'

        image = Image.open(filename)
        boxes, _ = self.mtcnn.detect(image)
        # boxes_lite = self.lite_face.lite_mtcnn.detect(image)
        if boxes is None:
            return render_template("members/add.html", member_image=image_url, detected_face=False)
        draw = ImageDraw.Draw(image)
        for box in boxes:
            draw.rectangle(box.tolist(), outline='red', width=int(image.width*0.01))
            break
        # for x, y, x2, y2, _ in boxes_lite:
        #     draw.rectangle((x.item(), y.item(), x2.item(), y2.item()), outline='blue', width=int(image.width*0.01))
        #     break
        filename = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), f'{image_id}_detected.jpg')
        image.save(filename)
        image_url = f'{base_url}/{image_id}_detected.jpg'
        return render_template("members/add.html", member_image=image_url, detected_face=True)

    def new(self):
        name = request.form.get('name')
        if not name:
            return jsonify(message='New member name was not provided!'), 404
        user_id = flask_login.current_user.id
        image_id = f'temp_member_{user_id}'
        exists = False
        if Members.query.filter_by(name=name).first():
            exists = True

        filename = name.replace(' ', '')
        file_dir = f'{user_id}\\{filename}'
        images_dir = os.path.join(current_app.config.get('IMAGES_DIR'), file_dir)
        embeddings_dir = os.path.join(current_app.config.get('EMBEDDINGS_DIR'), file_dir)
        Path(images_dir).mkdir(exist_ok=True, parents=True)
        Path(embeddings_dir).mkdir(exist_ok=True, parents=True)
        files_count = 0
        for _, _, files in os.walk(images_dir):
            files_count = len(files)

        if files_count == 0:
            image = os.path.join(current_app.config.get('IMAGES_DIR'), f'{file_dir}.jpg')
            temp_image = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), f'{image_id}.jpg')
            shutil.copy(temp_image, image)
            embedding_file = os.path.join(current_app.config.get('EMBEDDINGS_DIR'), f'{file_dir}.pt')
            img = Image.open(image)
            aligned = self.mtcnn(img)
            if aligned is None:
                Path(temp_image).unlink(missing_ok=True)
                return jsonify(message='No face on image was detected!'), 404
            aligned = aligned[0].unsqueeze(0)
            embeddings = self.resnet(aligned).detach()[0]
            torch.save(embeddings, embedding_file)

        files_count += 1
        image = os.path.join(images_dir, f'{filename}{files_count}.jpg')
        temp_image = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), f'{image_id}.jpg')
        shutil.copy(temp_image, image)
        embedding_file = os.path.join(embeddings_dir, f'{filename}{files_count}.pt')
        img = Image.open(image)
        aligned = self.lite_face.lite_mtcnn(img)
        if not aligned:
            Path(temp_image).unlink(missing_ok=True)
            return jsonify(message='No face on image was detected!'), 404
        torch.save(self.lite_face.get_embedding(aligned[0]), embedding_file)

        if not exists:
            # response = requests.post(url_for('members.add'))
            db = current_app.config.get('db')
            members_obj = self.create_members_obj((user_id, name, embeddings_dir, images_dir))
            db.session.add(members_obj)
            db.session.commit()

        Path(temp_image).unlink(missing_ok=True)
        Path(current_app.config.get('TEMP_UPLOAD_DIR'), f'{image_id}_detected.jpg').unlink(missing_ok=True)

        if exists:
            return jsonify(message=f'Added new photo for member {name}!')
        return jsonify(message='New member added!')

    # gui views
    def table(self):
        return render_template('members/members_table.html')

    def upload(self):
        return render_template('members/upload.html')
