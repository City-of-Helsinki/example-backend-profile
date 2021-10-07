from django.db import models
from helusers.models import AbstractUser


class User(AbstractUser):
    pass


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=255, null=True, blank=True)
