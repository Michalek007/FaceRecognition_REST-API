from flask import request, url_for, redirect, render_template, jsonify, current_app
import os
import struct

from app.blueprints import BlueprintSingleton
from scheduler.tasks import TaskType
from app.modules.face_recognition import recognize
from app.modules.image_utils import RGB565


class FaceRecognitionBp(BlueprintSingleton):
    """ Face recognition implementation. """
    MAX_IMAGES_COUNT = 5

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            cls._instance.img_count = 0
            cls._instance.test_img_count = 0
        return cls._instance

    # views
    def recognize(self):
        user_id = request.form.get('user_id')
        in_place = request.form.get('in_place')

        aligned = request.args.get('aligned')
        width = request.args.get('width')
        height = request.args.get('height')
        embedding = request.args.get('embedding')

        if not user_id:
            user_id = 'admin'

        print(request.content_type)
        print(request.content_length)
        print(aligned)
        print(width)
        print(height)

        if embedding:
            if request.content_length % 4 != 0:
                return jsonify(message="Length of embedding must be a multiple of 4")

            face_embedding = []
            for i in range(0, len(request.data), 4):
                byte_chunk = request.data[i:i + 4]
                float_value = struct.unpack('!f', bytes(byte_chunk))[0]
                face_embedding.append(float_value)

            print(face_embedding)
            if in_place:
                return {}
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

        image_id = f'{user_id}_{self.img_count}'
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
                return jsonify(message='File not found in request body!'), 404
        self.img_count += 1
        if self.img_count > self.MAX_IMAGES_COUNT - 1:
            self.img_count = 0

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
