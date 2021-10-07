from helusers.oidc import ApiTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import UserData
from users.permissions import IsSameUser
from users.serializers import UserDataSerializer


class MyUserDataView(RetrieveAPIView, UpdateAPIView):
    # APITokenAuthentication enables users with Bearer token to use this endpoint
    # SessionAuthentication enables users logged into the admin to use this endpoint
    authentication_classes = [ApiTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsSameUser]
    serializer_class = UserDataSerializer

    def get_object(self):
        try:
            return UserData.objects.get(user=self.request.user)
        except UserData.DoesNotExist:
            raise NotFound()
