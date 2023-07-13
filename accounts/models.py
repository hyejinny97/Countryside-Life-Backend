from django.db import models
from django.contrib.auth.models import AbstractUser

def user_image_path(instance, filename):
    # MEDIA_ROOT/profile_image/<filename> 경로로 업로드
    return f'profile_image/{filename}'

class User(AbstractUser):
    nickname = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to=user_image_path, blank=True)