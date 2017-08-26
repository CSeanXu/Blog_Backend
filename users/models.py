from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.default_model import random_nick_name


# Create your models here.
class UserProfile(AbstractUser):
    gender_choices = (
        ('male', '男'),
        ('female', '女'),
        ('unknown', '未知')
    )
    nick_name = models.CharField(max_length=100, default=random_nick_name)
    gender = models.CharField(choices=gender_choices, default='unknown', max_length=20)
    image = models.ImageField(upload_to='avatar/%Y/%m', max_length=100, default='avatar/avatar.png')
