import torch
from flask import request, url_for, redirect, render_template, jsonify, current_app
import os
from PIL import Image

from app.blueprints import BlueprintSingleton
from app.modules.face_recognition import mtcnn, resnet
from database.schemas import members_schema, members_many_schema, Members
from utils import DateUtil
from app.modules.data_class import TimestampDataClass


class FaceRecognitionBp(BlueprintSingleton):
    """ Face recognition implementation.
        Attributes:
            mtcnn: MTCNN model
            resnet: InceptionResnetV1 model
    """
    mtcnn = mtcnn
    resnet = resnet

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            cls._instance.img_count = 0
        return cls._instance

    # views
    def recognize(self):
        aligned = request.args.get('aligned')
        user_id = request.form.get('user_id')
        if not user_id:
            user_id = 'admin'

        # filename = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), f'cam_{user_id}_{self.img_count}.jpg')
        try:
            filename = os.path.join(current_app.config.get('TEMP_UPLOAD_DIR'), f'cam_{user_id}_{self.img_count}.jpg')
            request.files.get('imageFile').save(filename)
            self.img_count += 1
            if self.img_count > 4:
                self.img_count = 0
        except AttributeError:
            return jsonify(message=f'File not found in request body!'), 404

        img = Image.open(filename)
        self.mtcnn.keep_all = True
        aligned = self.mtcnn(img)
        recognized = False
        if aligned is not None:
            embeddings = self.resnet(aligned).detach()
            self.mtcnn.keep_all = False
    
            members_list = Members.query.filter_by(user_id=user_id)
            members_embeddings = []
            members_names = []
            for member in members_list:
                members_embeddings.append(torch.load(member.embedding))
                members_names.append(member.name)

            for embedding in embeddings:
                for i, member_embedding in enumerate(members_embeddings):
                    distance = (embedding - member_embedding).norm().item()
                    if distance < 1.0:
                        recognized = True
                        print(f'Recognized {members_names[i]}!')
        if not recognized:
            print("No members were recognized in the image!")

        # current_app.config.get('scheduler')
        return jsonify(message=f'Image uploaded successfully with name!')
