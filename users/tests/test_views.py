import pytest
from rest_framework import status

from users.models import UserData


@pytest.mark.django_db
class TestMyUserDataView:
    def test_get_userdata(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.get("/api/v1/myuserdata/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["pet_name"] is None
        assert response.data["birthday"] is None

    def test_update_userdata(self, api_client, user):
        api_client.force_authenticate(user=user)

        update_data = {"pet_name": "Fluffy", "birthday": "1990-01-15"}
        response = api_client.patch("/api/v1/myuserdata/", update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["pet_name"] == "Fluffy"
        assert response.data["birthday"] == "1990-01-15"

        user_data = UserData.objects.get(user=user)
        assert user_data.pet_name == "Fluffy"
        assert str(user_data.birthday) == "1990-01-15"
