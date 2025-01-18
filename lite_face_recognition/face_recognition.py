import torch
import torch.nn as nn
from PIL import Image
from pathlib import Path
import os
import math
from torchvision.transforms import ToTensor, Compose, Normalize
from typing import List
from lite_face_recognition.models import LiteFace100
from lite_face_recognition.lite_mtcnn import LiteMTCNN


class FaceRecognition:
    def __init__(self, model_pt_file: str, model: LiteFace100 = None, lite_mtcnn: LiteMTCNN = None):
        if model:
            self.model = model
        else:
            self.model = LiteFace100(3, (100, 100)).eval()
            self.model.load_state_dict(torch.load(model_pt_file, weights_only=True))

        if lite_mtcnn:
            self.lite_mtcnn = lite_mtcnn
        else:
            self.lite_mtcnn = LiteMTCNN().eval()

        self.known_embeddings = []
        self.names = []
        self.transform = Compose([ToTensor(), Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])])
        self.cosine_similarity = nn.CosineSimilarity(dim=0)
        self.margin = 0.97
        self.similarity_split = 0.8
        self.similarity_number = 4

    def create_copy(self):
        return FaceRecognition('', self.model, self.lite_mtcnn)

    def add_known_person(self, files: list, name: str, is_aligned: bool = False):
        images = []
        for i, file in enumerate(files):
            image = Image.open(file)
            if is_aligned:
                images.append(image)
                continue

            aligned = self.lite_mtcnn(image)
            if aligned:
                images.append(aligned[0])

        embeddings = []

        for image in images:
            embeddings.append(self.get_embedding(image))

        self.add_known_embedding(embeddings, name)

    def add_known_embedding(self, embeddings: List[torch.Tensor], name: str):
        self.known_embeddings.append(embeddings)
        self.names.append(name)

    def recognize(self, files: list, is_aligned: bool = False):
        recognized_all = [[] for _ in range(len(files))]
        for name in self.names:
            recognized_names = self.recognize_one(files, name, is_aligned)
            for i in range(len(recognized_all)):
                recognized_all[i] += recognized_names[i]

        return recognized_all

    def recognize_embeddings(self, embeddings: list):
        recognized_all = [[] for _ in range(len(embeddings))]
        for name in self.names:
            recognized_names = self.recognize_embeddings_one(embeddings, name)
            for i in range(len(recognized_all)):
                recognized_all[i] += recognized_names[i]

        return recognized_all

    def recognize_one(self, files: list, name: str, is_aligned: bool = False):
        target_embeddings_list = self.get_target_embeddings(files, is_aligned)
        return self.recognize_embeddings_one(target_embeddings_list, name)

    def recognize_embeddings_one(self, embeddings: List[List[torch.Tensor]], name: str):
        if name not in self.names:
            raise ValueError("No person found under this name!")

        known_embedding_index = self.names.index(name)
        recognized_names = []
        with torch.no_grad():
            for j, target_embeddings in enumerate(embeddings):
                recognized_names.append([])
                for embedding in target_embeddings:
                    recognized_count = 0
                    known_face_embeddings = self.known_embeddings[known_embedding_index]
                    recognized_max_count = len(known_face_embeddings)
                    distance_mean = 0
                    for known_embedding in known_face_embeddings:
                        distance = self.get_distance(known_embedding, embedding)
                        distance_mean += distance
                        if self.is_recognized(distance):
                            recognized_count += 1
                    threshold = self.similarity_number if self.similarity_number <= recognized_max_count else math.ceil(recognized_max_count*self.similarity_split)
                    if recognized_count >= threshold:
                        recognized_names[j].append(name)
                    else:
                        recognized_names[j].append('unknown')
                    distance_mean /= recognized_max_count
                    print(recognized_count)
                    print(distance_mean)
        return recognized_names

    def get_distance(self, known_embedding: torch.Tensor, target_embedding: torch.Tensor):
        distance = self.cosine_similarity(known_embedding, target_embedding)
        return distance

    def is_recognized(self, distance):
        return distance >= self.margin

    def get_embedding(self, image: Image):
        image = self.transform(image).unsqueeze(0)
        return self.model(image)[0]

    def get_target_embeddings(self, files: list, is_aligned: bool = False):
        images = []
        for file in files:
            image = Image.open(file)
            if is_aligned:
                if image.width != 100 or image.height != 100:
                    image = image.resize((100, 100))
                images.append([image])
                continue
            aligned = self.lite_mtcnn(image)
            images.append(aligned)

        target_embeddings_list = []
        for aligned_images in images:
            embeddings = []
            for img in aligned_images:
                embeddings.append(self.get_embedding(img))
            target_embeddings_list.append(embeddings)
        return target_embeddings_list

    def reset_known_embeddings(self):
        self.known_embeddings = []
        self.names = []
