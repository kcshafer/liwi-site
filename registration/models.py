from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_artist = models.BooleanField()
    type = models.CharField(max_length=80)