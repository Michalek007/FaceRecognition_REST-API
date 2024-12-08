from facenet_pytorch import InceptionResnetV1

resnet = InceptionResnetV1(pretrained='casia-webface').eval()
