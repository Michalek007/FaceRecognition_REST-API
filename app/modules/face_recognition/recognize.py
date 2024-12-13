from PIL import Image
import torch


from .mtcnn import mtcnn
from .resnet import resnet


class Recognize:
    def __init__(self):
        self.mtcnn = mtcnn
        self.resnet = resnet

    def run_resnet(self, filename: str, members_list: list, aligned: bool = False):
        img = Image.open(filename)
        if not aligned:
            # self.mtcnn.keep_all = True
            aligned_img = self.mtcnn(img)
            # self.mtcnn.keep_all = False
        else:
            aligned_img = img

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
                    if distance < 1.0:
                        recognized_members.append(members_names[i])
                        print(f'Recognized {members_names[i]}!')

        if not recognized_members:
            print("No members were recognized in the image!")

        return recognized_members


recognize = Recognize()
