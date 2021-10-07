from django.db import models
from helsinki_gdpr.models import SerializableMixin
from helusers.models import AbstractUser


class User(AbstractUser):
    pass


class UserData(SerializableMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=255, null=True, blank=True)

    serialize_fields = ({"name": "pet_name"},)
