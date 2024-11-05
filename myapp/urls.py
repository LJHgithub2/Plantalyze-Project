from django.urls import path

from .views.leaf_detections import LeafDetectionView  
from .views.disease_prediction import DiseasePredictionView
from .views.DB_manage import UserCreate,CreateDummyDataView,LatestAnalysisView, PlantAnalysisViewSet, PlantEnvironmentViewSet, PlantAnalysisCreateView, PlantEnvironmentCreateView



# from .views.gpt_solution
urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-create'),
    path('plant/leaf-detection', LeafDetectionView.as_view(), name='leaf_detections'),
    path('plant/disease-prediction', DiseasePredictionView.as_view(), name='disease_prediction'),
    # path('plant/disease-solution'),
    path('plant/get-plant/', PlantAnalysisViewSet.as_view({'get': 'list'}), name='get_plant'),
    path('plant/get-env/', PlantEnvironmentViewSet.as_view({'get': 'list'}), name='get_env'),
    path('plant/create/', PlantAnalysisCreateView.as_view(), name='create_plant_analysis'),
    path('env/create/', PlantEnvironmentCreateView.as_view(), name='create_plant_environment'),
    path('plant/latest-plant/', LatestAnalysisView.as_view(), name='latest-analysis'),
    path('plant/env-create_dummy_data/', CreateDummyDataView.as_view(), name='create_dummy_data'),
]