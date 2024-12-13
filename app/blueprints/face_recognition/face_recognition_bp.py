import torch
from flask import request, url_for, redirect, render_template, jsonify, current_app
import os
from PIL import Image

from app.blueprints import BlueprintSingleton
from app.modules.face_recognition import mtcnn, resnet
from database.schemas import members_schema, members_many_schema, Members
from utils import DateUtil
from app.modules.data_class import TimestampDataClass
from scheduler.tasks import TaskType
from app.modules.face_recognition import recognize
from app.modules.image_utils import RGB565


class FaceRecognitionBp(BlueprintSingleton):
    """ Face recognition implementation.
        Attributes:
            mtcnn: MTCNN model
            resnet: InceptionResnetV1 model
    """
    mtcnn = mtcnn
    resnet = resnet
    MAX_IMAGES_COUNT = 5

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            cls._instance.img_count = 0
            cls._instance.test_img_count = 0
        return cls._instance

    # views
    def recognize(self):
        aligned = request.args.get('aligned')
        user_id = request.form.get('user_id')
        in_place = request.form.get('in_place')
        if not user_id:
            user_id = 'admin'

        print(request.content_type)
        print(request.content_length)

        if request.content_type == 'application/octet-stream':
            image_id = f'{user_id}_{self.test_img_count}'
            filename = os.path.join('test_images', f'cam_{image_id}.jpg')
            rgb565 = RGB565(image_width=160, image_height=120)
            img = rgb565.to_pil_image(request.data)
            try:
                img.save(filename)
            except:
                pass
            self.test_img_count += 1
            if self.test_img_count >= 50:
                self.test_img_count = 0
            return jsonify(message='Image uploaded successfully!')

        image_id = f'{user_id}_{self.img_count}'
        try:
            filename = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), f'cam_{image_id}.jpg')
            request.files.get('imageFile').save(filename)
            self.img_count += 1
            if self.img_count > self.MAX_IMAGES_COUNT-1:
                self.img_count = 0
        except AttributeError:
            return jsonify(message='File not found in request body!'), 404

        if in_place:
            response, error = current_app.config.get('db_api').members_get(user_id=user_id)
            if error:
                return jsonify(message=error)
            members_list = response.json()
            return jsonify(recognized=recognize.run_resnet(filename, members_list, aligned))

        scheduler = current_app.config.get('scheduler')
        print(len(scheduler.get_jobs()))
        if len(scheduler.get_jobs()) >= self.MAX_IMAGES_COUNT:
            return jsonify(message='Images limit has been reached!'), 404
        scheduler.add_job(TaskType.face_recognition, image_id, 0.01, filename=filename, user_id=user_id, image_id=image_id, aligned=aligned)
        return jsonify(message='Image uploaded successfully!')
