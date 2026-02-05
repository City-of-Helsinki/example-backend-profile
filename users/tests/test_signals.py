import pytest

from users.models import User, UserData


@pytest.mark.django_db
class TestUserDataSignal:
    def test_userdata_created_on_user_creation(self):
        user = User.objects.create_user(
            username="testuser", email="testuser@example.com"
        )

        assert UserData.objects.filter(user=user).exists()

        user_data = UserData.objects.get(user=user)
        assert user_data.user == user
        assert user_data.pet_name is None
        assert user_data.birthday is None
