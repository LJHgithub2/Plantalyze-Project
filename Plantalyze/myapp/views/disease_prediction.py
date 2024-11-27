import torch
import torch.nn as nn
from PIL import Image
import torchvision.transforms.functional as TF
import pandas as pd
import numpy as np
from torchsummary import summary

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import os
import logging
logger = logging.getLogger(__name__)

class DiseasePredictionView(APIView):
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static','model', 'plant_disease_v1.pt')
    model = None
    disease_info_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static','meta', 'disease_info.csv')
    disease_info = None

    @classmethod
    def initialize_model(cls):
        if not os.path.exists(cls.model_path):
            logger.error("Model file not found at path: %s", cls.model_path)
            raise FileNotFoundError("Model file not found.")
        
        targets_size = 39
        cls.model = CNN(targets_size)
        cls.model.load_state_dict(torch.load(cls.model_path))
        cls.model.eval()
        logger.info("Model loaded successfully from %s", cls.model_path)
        cls.disease_info = pd.read_csv(cls.disease_info_path, encoding="utf-8")

    def post(self, request, *args, **kwargs):
        image_path = request.data.get("image_path")
        if not image_path:
            return Response({"error": "No image path provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        full_image_path = os.path.join(os.path.dirname(__file__),"../static/image/", image_path)
        
        if not os.path.exists(full_image_path):
            return Response({"error": "Image file not found."}, status=status.HTTP_404_NOT_FOUND)
        
        analysis_result = self.disease_prediction(full_image_path)
        return Response({
            "image_path": image_path,
            "analysis": analysis_result
        }, status=status.HTTP_200_OK)

    
    def disease_prediction(self,image_path):
        image = Image.open(image_path)
        image = image.resize((224, 224))
        input_data = TF.to_tensor(image)
        input_data = input_data.view((-1, 3, 224, 224))
        output = self.model(input_data)
        output = output.detach().numpy()
        index = np.argmax(output)
        pred_csv = {
            "plant_type":self.disease_info["plant_type"][index],
            "disease_name":self.disease_info["disease_name"][index],
            "explanation":self.disease_info["explanation"][index],
            "solution":self.disease_info["solution"][index],
            "image_url":self.disease_info["image_url"][index],
        }
        return pred_csv

class CNN(nn.Module):
    def __init__(self, K):
        super(CNN, self).__init__()
        self.conv_layers = nn.Sequential(
            # conv1
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(2),
            # conv2
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2),
            # conv3
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(2),
            # conv4
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.MaxPool2d(2),
        )

        self.dense_layers = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(50176, 1024),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(1024, K),
        )

    def forward(self, X):
        out = self.conv_layers(X)

        # Flatten
        out = out.view(-1, 50176)

        # Fully connected
        out = self.dense_layers(out)

        return out
    
DiseasePredictionView.initialize_model()