from django.db import models
class User_info(models.Model):
    user_id=models.AutoField(primary_key=True)
    cuisine_name=models.CharField(max_length=264)
    food_type=models.CharField(max_length=264)
    allergies=models.CharField(max_length=264, default="No allergies")
    height=models.DecimalField(max_digits=20, decimal_places=15)
    weight=models.DecimalField(max_digits=20, decimal_places=15)
    age=models.IntegerField()
    goals=models.CharField(max_length=10000)
    issues=models.CharField(max_length=10000)
    gender=models.CharField(max_length=264)
# Create your models here.
