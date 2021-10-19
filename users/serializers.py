from rest_framework import serializers

from users.models import UserData


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["pet_name", "birthday"]
