from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

#DefaultUser:AbstractUser  = get_user_model()
class DefaultUser(AbstractUser):
    pass