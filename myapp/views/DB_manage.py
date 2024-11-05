# analysis/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, generics
from ..models import PlantAnalysis, PlantEnvironment
from ..serializers import PlantAnalysisSerializer, PlantEnvironmentSerializer
# myapp/views.py
from rest_framework.views import APIView
from datetime import datetime, timedelta
import random


class LatestAnalysisView(APIView):
    def get(self, request, *args, **kwargs):
        latest_analysis = PlantAnalysis.objects.order_by('-created_at').first()
        if latest_analysis:
            serializer = PlantAnalysisSerializer(latest_analysis, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'error': 'No analysis found'}, status=404)

class PlantAnalysisViewSet(viewsets.ModelViewSet):
    queryset = PlantAnalysis.objects.all()
    serializer_class = PlantAnalysisSerializer

class PlantEnvironmentViewSet(viewsets.ModelViewSet):
    queryset = PlantEnvironment.objects.all()
    serializer_class = PlantEnvironmentSerializer

class PlantAnalysisCreateView(generics.CreateAPIView):
    queryset = PlantAnalysis.objects.all()
    serializer_class = PlantAnalysisSerializer

class PlantEnvironmentCreateView(generics.CreateAPIView):
    queryset = PlantEnvironment.objects.all()
    serializer_class = PlantEnvironmentSerializer


class CreateDummyDataView(APIView):
    def post(self, request, *args, **kwargs):
        now = datetime.now()
            # 현재 시간을 5분 단위로 맞춤
        nearest_5_min = now - timedelta(minutes=now.minute % 5, seconds=now.second, microseconds=now.microsecond)
            
        for _ in range(20):
            temperature = random.randint(20, 50)
            humidity = random.randint(50, 300)
            illumination = random.randint(50, 400)
            PlantEnvironment.objects.create(
                date=nearest_5_min,
                temperature=temperature,
                humidity=humidity,
                illumination=illumination
            )
            # 다음 데이터는 5분 뒤로 설정
            nearest_5_min += timedelta(minutes=5)
            
        return Response({"message": "20 dummy records created successfully"}, status=201)
    
    # analysis/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import UserSerializer

class UserCreate(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)