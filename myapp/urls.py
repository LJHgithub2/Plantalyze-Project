from django.urls import path

from .views.leaf_detections import LeafDetectionView  
from .views.disease_prediction import DiseasePredictionView
# from .views.gpt_solution
urlpatterns = [
    path('plant/leaf-detection', LeafDetectionView.as_view(), name='leaf_detections'),
    path('plant/disease-prediction', DiseasePredictionView.as_view(), name='disease_prediction'),
    # path('plant/disease-solution'),
]