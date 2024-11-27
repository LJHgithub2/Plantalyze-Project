# analysis/models.py

from django.db import models

class PlantAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    skip_processing = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    plant_type = models.CharField(max_length=255, null=True)
    predicted_disease = models.CharField(max_length=255, null=True)
    risk_level = models.IntegerField(null=True)
    current_status = models.CharField(max_length=255, null=True)
    improvement_plan = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    # 바운딩 박스의 좌표값을 저장할 필드들
    bbox_left_top_x = models.FloatField(null=True)
    bbox_left_top_y = models.FloatField(null=True)
    bbox_right_bottom_x = models.FloatField(null=True)
    bbox_right_bottom_y = models.FloatField(null=True)

    def __str__(self):
        return f"{self.image}"


class PlantEnvironment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    illumination = models.IntegerField()

    def __str__(self):
        return f"{self.date} - Temp: {self.temperature}, Humidity: {self.humidity}, Illumination: {self.illumination}"
