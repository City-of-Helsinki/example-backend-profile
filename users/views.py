from django.http import Http404
from helsinki_gdpr.models import SerializableMixin
from helsinki_gdpr.views import GDPRAPIView
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


class ExampleGDPRAPIView(GDPRAPIView):
    """GDPRAPIView which finds UserData instance by user UUID

    This view is customized because helsinki-profile-gdpr-api expects the URL to
    have the id of the GDPR_API_MODEL. In this example we have the user's UUID but
    need to find the corresponding UserData instance instead."""

    def get_object(self) -> SerializableMixin:
        """Get the userdata corresponding the user UUID provided in the URL"""
        try:
            userdata = UserData.objects.get(user__uuid=self.kwargs["uuid"])
        except UserData.DoesNotExist:
            raise Http404("No userdata")

        self.check_object_permissions(self.request, userdata)
        return userdata