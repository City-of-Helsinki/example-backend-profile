from django.db import models
from helsinki_gdpr.models import SerializableMixin
from helusers.models import AbstractUser


class User(AbstractUser, SerializableMixin):
    serialize_fields = (
        {"name": "first_name"},
        {"name": "last_name"},
        {"name": "email"},
    )


class UserData(SerializableMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    serialize_fields = (
        {"name": "user"},
        {"name": "pet_name"},
        {"name": "birthday"},
    )
