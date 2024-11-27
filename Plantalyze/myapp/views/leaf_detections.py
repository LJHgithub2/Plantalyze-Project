from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ultralytics import YOLO
import os
import logging

# Logger 설정
logger = logging.getLogger(__name__)

class LeafDetectionView(APIView):
    # 클래스 변수로 모델을 초기화
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static','model', 'leaf_detection.pt')
    model = None

    @classmethod
    def initialize_model(cls):
        if not os.path.exists(cls.model_path):
            logger.error("Model file not found at path: %s", cls.model_path)
            raise FileNotFoundError("Model file not found.")
        
        cls.model = YOLO(cls.model_path)
        logger.info("Model loaded successfully from %s", cls.model_path)

    def post(self, request, *args, **kwargs):
        image_path = request.data.get("image_path")
        if not image_path:
            return Response({"error": "No image path provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        full_image_path = os.path.join(os.path.dirname(__file__),"../static/image/", image_path)
        
        if not os.path.exists(full_image_path):
            return Response({"error": "Image file not found."}, status=status.HTTP_404_NOT_FOUND)
        
        analysis_result = self.detection_leaf(full_image_path)
        return Response({
            "image_path": image_path,
            "analysis": analysis_result
        }, status=status.HTTP_200_OK)
    
    def detection_leaf(self, image_path):
        if not self.model:
            return {"error": "Model is not loaded."}
        
        results = self.model(image_path, conf=0.3)
        
        # 결과를 처리하여 원하는 형식으로 반환
        analyzed_data = []
        class_names = ['leaf']
        
        for result in results:
            boxes = result.boxes.xyxy  # 바운딩 박스 좌표
            confidences = result.boxes.conf  # 신뢰도
            class_nums = result.boxes.cls  # 클래스 번호
            
            for box, confidence, class_num in zip(boxes, confidences, class_nums):
                bbox = box[:4].tolist()  # 바운딩 박스 좌표를 리스트로 변환
                class_name = class_names[int(class_num)]
                analyzed_data.append({
                    'bbox': bbox,
                    'class_name': class_name,
                    'confidence': float(confidence)
                })
        
        return analyzed_data

# 서버 시작 시 모델 초기화
LeafDetectionView.initialize_model()
