from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# DefaultUser:AbstractUser  = get_user_model()


class DefaultUser(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=False)
    patronymic = models.CharField(max_length=25, blank=True)
