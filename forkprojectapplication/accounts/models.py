from django.contrib.auth.models import AbstractUser
from django.db import models

from forkprojectapplication.common.models import CustomBaseModel


# Create your models here.
class UserProfile(CustomBaseModel):
    pass


class CustomUser(AbstractUser):
    user_profile = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    