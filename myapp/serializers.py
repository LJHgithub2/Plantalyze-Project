# analysis/serializers.py
from datetime import datetime
from rest_framework import serializers
from .models import PlantAnalysis, PlantEnvironment
from django.core.files.storage import default_storage
from django.db.models.signals import post_save
from django.dispatch import receiver
import numpy as np
from ultralytics import YOLO
from django.conf import settings
import torchvision.transforms.functional as TF
import os
import torch
import torch.nn as nn
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import json
from PIL import Image
from datetime import datetime, timedelta
from google.cloud import translate

# analysis/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


def get_env_info():
    # 현재 날짜 가져오기
    current_date = datetime.now().date()

    # 3일 이전 날짜 계산
    three_days_ago = current_date - timedelta(days=3)

    # PlantEnvironment 모델의 최근 3일 데이터 가져오기
    recent_data = PlantEnvironment.objects.filter(date__gte=three_days_ago)

    # 각 필드의 데이터를 문자열로 변환하여 원하는 형식으로 구성
    temperature_str = ', '.join(str(data.temperature) for data in recent_data)
    humidity_str = ', '.join(str(data.humidity) for data in recent_data)
    illumination_str = ', '.join(str(data.illumination) for data in recent_data)

    # 원하는 형식으로 데이터 문자열 구성
    data_string = f"The temperature changed {temperature_str} every two hours.\n"
    data_string += f"The humidity changed {humidity_str} every two hours.\n"
    data_string += f"The illumination changed {illumination_str} every two hours.\n"
    data_string += f"The following is information about the illuminance, humidity, and temperature of the environment in which the plant recently grew.\n"

    # 각 필드의 데이터를 리스트로 수집하여 딕셔너리로 구성
    data_dict = {
        "temperature": [data.temperature for data in recent_data],
        "humidity": [data.humidity for data in recent_data],
        "illumination": [data.illumination for data in recent_data]
    }

    # 변경된 데이터 딕셔너리 출력
    return data_string

def nms(boxes, confidences, iou_threshold=0.5):
    if len(boxes) == 0:
        return []

    # 바운딩 박스 좌표를 numpy 배열로 변환
    boxes = np.array(boxes)
    confidences = np.array(confidences)

    # 바운딩 박스의 좌표와 넓이를 계산
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    # 신뢰도 점수를 기준으로 정렬
    order = confidences.argsort()[::-1]

    keep = []  # 유지할 바운딩 박스의 인덱스를 저장할 리스트

    while order.size > 0:  # 남은 바운딩 박스가 없을 때까지 반복
        i = order[0]  # 현재 가장 높은 신뢰도를 가진 바운딩 박스의 인덱스
        keep.append(i)

        # 현재 박스와 나머지 박스의 좌표 계산
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        # 교차 영역의 너비와 높이 계산
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        inter = w * h  # 교차 영역의 면적

        # IoU (Intersection over Union) 계산
        iou = inter / (areas[i] + areas[order[1:]] - inter)  # 교차 영역 / 합집합 영역

        # IoU가 임계값 이하인 인덱스를 찾음
        inds = np.where(iou <= iou_threshold)[0]

        # 남은 바운딩 박스 중에서 현재 처리한 박스를 제외한 박스들로 order를 갱신
        order = order[inds + 1]

    return keep

from PIL import Image, ImageDraw

def save_image_with_bbox(original_image_path, output_folder, box_coordinates):
    """
    바운딩 박스가 포함된 이미지를 저장하는 함수
    :param original_image_path: 원본 이미지 파일 경로
    :param output_folder: 결과 이미지를 저장할 폴더 경로
    :param box_coordinates: 바운딩 박스 좌표 [x1, y1, x2, y2]
    """
    # 결과를 이용하여 새로운 이미지를 저장할 파일명
    output_image_filename = os.path.basename(original_image_path)

    # 바운딩 박스를 포함한 이미지 저장
    original_image = Image.open(original_image_path)
    output_image = original_image.copy()

    # 바운딩 박스 그리기
    draw = ImageDraw.Draw(output_image)
    draw.rectangle(box_coordinates, outline='red', width=2)  # 바운딩 박스 그리기

    # 새로운 이미지 저장
    output_image.save(output_folder)

    print(f"새로운 이미지가 '{output_folder}' 경로에 저장되었습니다.")

def generate_image_filename():
    """
    현재 시간을 기준으로 이미지 파일명을 생성하는 함수
    """
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y%m%d%H%M%S")  # 형식화된 시간 문자열 생성 (예: 20240613153045)
    image_filename = f"image_{timestamp}.jpg"  # 이미지 파일명 생성
    return image_filename

def get_env_over(water, light, wind):
    string = "The recent environment of the plant is "
    string += "Give " + str(int(water)) + " ml of water a day, "
    string += "provide " + str(int(light)) + " hours of lighting a day, "
    string += "and let the wind blow for " + str(int(wind)) + " hours a day."
    return string


def translate_text(
    text: str = "hello world", project_id: str = "ai-project-423805"
) -> translate.TranslationServiceClient:
    
    dotenv_path = 'C:\code\Plantalyze\myapp\static\env\gpt.env'

    load_dotenv(dotenv_path, verbose=True)
    api_key = os.getenv('GCP_JSON_KEY_PATH')

    """Translating Text."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_key

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": "ko",
        }
    )

    # Display the translation for each input text provided
    # for translation in response.translations:
    #     print(f"Translated text: {translation.translated_text}")

    return response

@receiver(post_save, sender=PlantAnalysis)
def process_image(sender, instance, created, **kwargs):
    if not instance.skip_processing:
        # 만약 이미지가 새로 생성되었을 때만 처리를 실행하려면 created 매개변수를 사용합니다.
        if created:

            # 학습된 가중치 파일 적용
            model = YOLO(os.path.join(os.path.dirname(os.path.dirname(__file__)),'myapp','static','model', 'leaf_detection_v2.pt'))
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'myapp','static','model', 'plant_disease_v1.pt')
            disease_info_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'myapp','static','meta', 'disease_info(eng).csv')
            extensions = ["json", "txt", "jpg", "JPG", "png", "PNG"]
            # 이미지 파일의 전체 URL 생성
            MEDIA_ROOT = settings.MEDIA_ROOT
            path = os.path.join(MEDIA_ROOT,os.path.basename(instance.image.url))
            results = model(path, conf=0.01)

            for result in results[:1]:
                boxes = result.boxes.xyxy[:4].tolist()  # 바운딩 박스 좌표

            base_name=generate_image_filename()
            image_filename = "C:\code\Plantalyze\media\\"+base_name

            save_image_with_bbox(path, image_filename, boxes[0])
            
            targets_size = 39
            model = CNN(targets_size)
            model.load_state_dict(torch.load(model_path))
            model.eval()
            disease_info = pd.read_csv(disease_info_path, encoding="cp1252")#영어
            #disease_info = pd.read_csv(disease_info_path, encoding="utf-8")#한글
            
            image = Image.open(path)
            cropped_image = image.crop((boxes[0][0], boxes[0][1], boxes[0][2], boxes[0][3]))
            image = cropped_image.resize((224, 224))
            input_data = TF.to_tensor(image)
            input_data = input_data.view((-1, 3, 224, 224))
            output = model(input_data)
            output = output.detach().numpy()
            index = np.argmax(output)
            pred_csv = {
                "disease_name":disease_info["disease_name"][index],# 식물: 질병 형식으로 나와있음
                "explanation":disease_info["description"][index],
                "solution":disease_info["Possible Steps"][index],
            }
            # 원하는 형식으로 데이터 문자열 구성
            print(pred_csv['disease_name'].split(':')[0],pred_csv['disease_name'].split(':')[1])
            data_string = f"The plant_type detected by the video analyzer is {pred_csv['disease_name'].split(':')[0]}.\n"
            data_string += f"The detected disease is {pred_csv['disease_name'].split(':')[1]}, which is explained as '{pred_csv['explanation']}'.\n"
            print(pred_csv)

            
            dotenv_path = 'C:\code\Plantalyze\myapp\static\env\gpt.env'

            load_dotenv(dotenv_path, verbose=True)

            
            api_key = os.getenv('GPT_API_KEY')
            Project = os.getenv('ORG_ID')

            client = OpenAI(
            organization=Project,
            api_key=api_key
            )
            data_string += get_env_info()
            json_data = chat_gpt(client,data_string)
            parsed_data = json.loads(json_data)
            parsed_data['bbox_left_top_x'] = boxes[0][0]
            parsed_data['bbox_left_top_y'] = boxes[0][1]
            parsed_data['bbox_right_bottom_x'] = boxes[0][2]
            parsed_data['bbox_right_bottom_y'] = boxes[0][3]

            print(parsed_data)

            instance.plant_type = parsed_data['plant_type']
            instance.predicted_disease = parsed_data['predicted_disease']
            instance.risk_level = parsed_data['risk_level']
            instance.current_status = translate_text(parsed_data['current_status']).translations[0].translated_text
            instance.improvement_plan = translate_text(parsed_data['improvement_plan']).translations[0].translated_text
            instance.bbox_left_top_x = parsed_data['bbox_left_top_x']
            instance.bbox_left_top_y = parsed_data['bbox_left_top_y']
            instance.bbox_right_bottom_x = parsed_data['bbox_right_bottom_x']
            instance.bbox_right_bottom_y = parsed_data['bbox_right_bottom_y']
            instance.image = base_name
            
            # 모델 인스턴스 저장
            instance.save()

    else:
        if created:

            # 학습된 가중치 파일 적용
            model = YOLO(os.path.join(os.path.dirname(os.path.dirname(__file__)),'myapp','static','model', 'leaf_detection_v2.pt'))
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'myapp','static','model', 'plant_disease_v1.pt')
            disease_info_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'myapp','static','meta', 'disease_info(eng).csv')
            
            # 이미지 파일의 전체 URL 생성
            MEDIA_ROOT = settings.MEDIA_ROOT
            path = os.path.join(MEDIA_ROOT,os.path.basename(instance.image.url))
            results = model(path, conf=0.01)

            for result in results[:1]:
                boxes = result.boxes.xyxy[:4].tolist()  # 바운딩 박스 좌표

            base_name=generate_image_filename()
            image_filename = "C:\code\Plantalyze\media\\"+base_name

            save_image_with_bbox(path, image_filename, boxes[0])
            
            targets_size = 39
            model = CNN(targets_size)
            model.load_state_dict(torch.load(model_path))
            model.eval()
            disease_info = pd.read_csv(disease_info_path, encoding="cp1252")#영어
            #disease_info = pd.read_csv(disease_info_path, encoding="utf-8")#한글
            
            image = Image.open(path)
            cropped_image = image.crop((boxes[0][0], boxes[0][1], boxes[0][2], boxes[0][3]))
            image = cropped_image.resize((224, 224))
            input_data = TF.to_tensor(image)
            input_data = input_data.view((-1, 3, 224, 224))
            output = model(input_data)
            output = output.detach().numpy()
            index = np.argmax(output)
            pred_csv = {
                "disease_name":disease_info["disease_name"][index],# 식물: 질병 형식으로 나와있음
                "explanation":disease_info["description"][index],
                "solution":disease_info["Possible Steps"][index],
            }
            # 데이터 문자열 구성
            try:
                # `disease_name` 값을 ':'를 기준으로 분리하여 데이터 문자열을 구성
                plant_type = pred_csv['disease_name'].split(':')[0]
                disease_name = pred_csv['disease_name'].split(':')[1]
                
                data_string = f"The plant_type detected by the video analyzer is {plant_type}.\n"
                data_string += f"The detected disease is {disease_name}, which is explained as '{pred_csv['explanation']}'.\n"
                data_string += "The following is information about the illuminance, humidity, and temperature of the environment in which the plant recently grew.\n"
            except Exception as e:
                # 오류 발생 시 예외 처리
                data_string = "No plants detected. Please request analysis again.\n"

            print(data_string)


            
            dotenv_path = 'C:\code\Plantalyze\myapp\static\env\gpt.env'

            load_dotenv(dotenv_path, verbose=True)
            
            api_key = os.getenv('GPT_API_KEY')
            Project = os.getenv('ORG_ID')

            client = OpenAI(
            organization=Project,
            api_key=api_key
            )
            data_string += get_env_over(instance.bbox_left_top_x,# 물
                                    instance.bbox_left_top_y,# 조도
                                    instance.bbox_right_bottom_x,#바람
                                    )
            json_data = chat_gpt(client,data_string)
            parsed_data = json.loads(json_data)
            parsed_data['bbox_left_top_x'] = boxes[0][0]
            parsed_data['bbox_left_top_y'] = boxes[0][1]
            parsed_data['bbox_right_bottom_x'] = boxes[0][2]
            parsed_data['bbox_right_bottom_y'] = boxes[0][3]


            instance.plant_type = parsed_data['plant_type']
            instance.predicted_disease = parsed_data['predicted_disease']
            instance.risk_level = parsed_data['risk_level']
            instance.current_status = translate_text(parsed_data['current_status']).translations[0].translated_text
            instance.improvement_plan = translate_text(parsed_data['improvement_plan']).translations[0].translated_text
            instance.bbox_left_top_x = parsed_data['bbox_left_top_x']
            instance.bbox_left_top_y = parsed_data['bbox_left_top_y']
            instance.bbox_right_bottom_x = parsed_data['bbox_right_bottom_x']
            instance.bbox_right_bottom_y = parsed_data['bbox_right_bottom_y']
            instance.image = base_name

            # 모델 인스턴스 저장
            instance.save()


def chat_gpt(client, info_string):
    print("=" * 40+" 질문 내용 " +"="*40)
    print(info_string)
    print("="*85)
    #응답 받기
    response = client.chat.completions.create(
        model = "gpt-4-turbo",
        # model = "gpt-3.5-turbo-0125",
        messages =[
            {
                "role":"system",
                "content":"Are you a plant expert. Response in json format\
                with Answer 'plant_type','predicted_disease ','risk_level','current_status','improvement_plan', 'Lack of water'\
                , 'Lack of lighting', 'Lack of wind '."
            },
            {
                "role":"system",
                "content":"The 'risk_level' item is rated only from 0 to 5, with 0 being healthy\
                and 5 being bad."
            },
            {
                "role":"system",
                "content":"The 'Current Status' item describes the current status of the plant."
            },
            {
                "role":"system",
                "content":"The 'Improvement Plan' item suggests ways to grow plants more healthily."
            },
            {
                "role":"system",
                "content":"The 'Lack of water' item can be displayed as a number from 0 to 5 and\
                specifies the amount of water the plant currently needs. 0 means to continue the\
                current watering cycle and 5 means you need to water more."
            },
            {
                "role":"system",
                "content":"The 'Lack of Light' item can be displayed with a number from 0 to 5 and\
                specifies the amount of lighting the plant currently needs. 0 means to keep the\
                current lighting and 5 means to give more lighting."
            },
            {
                "role":"system",
                "content":"The 'Lack of wind' item can be displayed with numbers 0 to 5 and\
                specifies the amount of wind that the current plant needs. 0 means to keep\
                the current wind and 5 means to give more wind."
            },
            {
                "role":"user",
                "content":info_string
            }
        ],
        temperature=0,
        max_tokens = 1000,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0,

        # response_format 지정하기
        response_format = {"type":"json_object"}
    )

    
    print("=" * 40+" 답변 내용 " +"="*40)
    print(response.choices[0].message.content)
    print("="*85)
    return response.choices[0].message.content

class PlantAnalysisSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True) # 이미지 필드 추가
    class Meta:
        model = PlantAnalysis
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    def create(self, validated_data):
        image = validated_data.pop('image', None)  # 이미지 필드 추출

        # 이미지 파일을 처리하는 로직
        if image:
            # 현재 날짜와 시간을 이용하여 파일 이름 생성
            current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
            file_name = f'image_{current_datetime}.jpg'  # 확장자는 이미지 파일의 확장자로 변경해야 합니다.

            # 이미지를 저장할 디렉토리 경로 설정
            file_path = f'{file_name}'

            # 이미지 파일을 서버에 저장
            default_storage.save(file_path, image)

            # 데이터베이스에 이미지 파일의 경로를 저장
            validated_data['image'] = file_path

        return super().create(validated_data)
    



class PlantEnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantEnvironment
        fields = '__all__'



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
