from django.urls import path

from .views.leaf_detections import LeafDetectionView  
# from .views.disease_prediction
# from .views.gpt_solution
urlpatterns = [
    path('plant/leaf-detection', LeafDetectionView.as_view(), name='plant-analyze'),
    # path('plant/disease-prediction'),
    # path('plant/disease-solution'),
]