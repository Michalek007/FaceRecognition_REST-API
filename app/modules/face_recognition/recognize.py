from PIL import Image
import torch
from torchvision.transforms import functional as F
from torch.nn.functional import interpolate
import numpy as np
from typing import List

from .mtcnn import mtcnn
from .resnet import resnet
from .lite_face import lite_face


class Recognize:
    def __init__(self):
        self.mtcnn = mtcnn
        self.resnet = resnet
        self.lite_face = lite_face

    def run_resnet(self, filename: str, members_list: list, aligned: bool = False):
        img = Image.open(filename)
        if not aligned:
            aligned_img = self.mtcnn(img)
        else:
            img = F.to_tensor(np.float32(img))
            img = (img - 127.5) / 128.0
            aligned_img = img.unsqueeze(0)
            aligned_img = interpolate(aligned_img, (160, 160), mode='area')

        recognized_members = []
        if aligned_img is not None:
            embeddings = self.resnet(aligned_img).detach()

            members_embeddings = []
            members_names = []
            for member in members_list:
                members_embeddings.append(torch.load(member['embedding']))
                members_names.append(member['name'])

            for embedding in embeddings:
                for i, member_embedding in enumerate(members_embeddings):
                    distance = (embedding - member_embedding).norm().item()
                    print(members_names[i])
                    print(distance)
                    if distance < 1.1:
                        recognized_members.append(members_names[i])
                        print(f'Recognized {members_names[i]}!')

        if not recognized_members:
            print("No members were recognized in the image!")

        return recognized_members

    def run_lite_face(self, embedding: List[float], members_list: list):
        pass


recognize = Recognize()
