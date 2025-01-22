from flask import request, url_for, redirect, render_template, jsonify, current_app
import flask_login
import os
import struct
import torch
from collections import defaultdict

from app.blueprints import BlueprintSingleton
from scheduler.tasks import TaskType
from database.schemas import User
from app.modules.face_recognition import recognize
from app.modules.image_utils import RGB565


class FaceRecognitionBp(BlueprintSingleton):
    """ Face recognition implementation. """
    MAX_IMAGES_COUNT = 5
    MAX_EMBEDDINGS_COUNT = 5
    EMBEDDING_LEN = 128

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            cls._instance.test_img_count = 0
            cls._instance.user_counts = defaultdict(lambda: [0, 0])  # img_count, embedding_count
        return cls._instance

    # views
    def recognize(self):
        device_id = request.args.get('device_id')
        aligned = request.args.get('aligned')
        width = request.args.get('width')
        height = request.args.get('height')
        embedding = request.args.get('embedding')
        in_place = request.args.get('in_place')

        user_id = flask_login.current_user.id
        if user_id == current_app.config.get('TOKEN'):
            user = User.query.filter_by(device_id=device_id).first()
            if not user:
                return jsonify(message="Unauthorised device id. "), 404
            user_id = user.username

        scheduler = current_app.config.get('scheduler')
        scheduler_jobs = scheduler.get_jobs()

        print(user_id)
        print(request.content_type)
        print(request.content_length)
        print(aligned)
        print(width)
        print(height)

        if embedding:
            embedding_id = f'{user_id}_{self.user_counts[user_id][1]}_emb'
            if len([job for job in scheduler_jobs if job.id == embedding_id]):
                return jsonify(message='Facial recognition workers limit has been reached!'), 404

            if request.content_length != self.EMBEDDING_LEN * 4:
                return jsonify(message="Length of face embedding must be 128!")

            face_embedding = []
            for i in range(request.content_length//4):
                face_embedding.append(struct.unpack('>f', request.data[4*i:4*i+4])[0])
            print(face_embedding)

            filename = os.path.join('temp', f'{embedding_id}.pt')
            face_embedding = torch.tensor(face_embedding, dtype=torch.float)
            torch.save(face_embedding, filename)

            self.user_counts[user_id][1] += 1
            if self.user_counts[user_id][1] >= self.MAX_EMBEDDINGS_COUNT:
                self.user_counts[user_id][1] = 0

            if in_place:
                response, error = current_app.config.get('db_api').members_get(user_id=user_id)
                if error:
                    return jsonify(message=error)
                members_list = response.json()
                return jsonify(recognized=recognize.run_lite_face(filename, members_list))

            scheduler.add_job(TaskType.face_recognition, embedding_id, 0.01, filename=filename, user_id=user_id, scheduler_job_id=embedding_id, aligned=aligned, embedding=embedding)
            return jsonify(message='Embedding uploaded successfully!')

        if request.content_type == 'application/octet-stream' and not aligned:
            image_id = f'{user_id}_{self.test_img_count}'
            filename = os.path.join('test_images', f'cam_{image_id}.jpg')
            if not width and not height:
                width = 160
                height = 120
            rgb565 = RGB565(image_width=int(width), image_height=int(height))
            img = rgb565.to_pil_image(request.data)
            try:
                img.save(filename)
            except OSError:
                pass
            self.test_img_count += 1
            if self.test_img_count >= 200:
                self.test_img_count = 0
            return jsonify(message='Image uploaded successfully!')

        image_id = f'{user_id}_{self.user_counts[user_id][0]}'
        if len([job for job in scheduler_jobs if job.id == image_id]):
            return jsonify(message='Facial recognition workers limit has been reached!'), 404
        if request.content_type == 'application/octet-stream':
            filename = os.path.join('temp', f'cam_{image_id}.jpg')
            if not width or not height:
                return jsonify(message="Missing args: width & height!"), 404
            rgb565 = RGB565(image_width=int(width), image_height=int(height))
            img = rgb565.to_pil_image(request.data)
            img.save(filename)
        else:
            try:
                filename = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), f'cam_{image_id}.jpg')
                request.files.get('imageFile').save(filename)
            except AttributeError:
                return jsonify(message='Image file not found in request body!'), 404

        self.user_counts[user_id][0] += 1
        if self.user_counts[user_id][0] >= self.MAX_IMAGES_COUNT:
            self.user_counts[user_id][0] = 0

        if in_place:
            response, error = current_app.config.get('db_api').members_get(user_id=user_id)
            if error:
                return jsonify(message=error)
            members_list = response.json()
            return jsonify(recognized=recognize.run_resnet(filename, members_list, aligned))

        scheduler.add_job(TaskType.face_recognition, image_id, 0.01, filename=filename, user_id=user_id, scheduler_job_id=image_id, aligned=aligned, embedding=embedding)
        return jsonify(message='Image uploaded successfully!')
