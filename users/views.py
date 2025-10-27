import datetime

import requests
from django.conf import settings
from helusers.oidc import ApiTokenAuthentication
from requests import RequestException
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
            raise NotFound() from None  # noqa: B904


class FillMyBirthday(APIView):
    """View which fills the birthday field in the user's UserData

    The client should make a POST request to this view with a payload dictionary
    with one key `api_token` that should be an Tunnistamo API Token for Helsinki
    Profile backend.

    This view then queries the Helsinki Profile GraphQL for the users national
    identification number and determines the birthday from that. The "loa"-claim
    in the api_token has to be "substantial" or "high" in order to make the query
    successfully.

    This view is just an example how to use an API Token to query the Helsinki
    Profile. It's not modularised or use any GraphQL client libraries."""

    authentication_classes = [ApiTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsSameUser]

    def post(self, request, *args, **kwargs):
        profile_api_token = request.data.get("api_token")
        if not profile_api_token:
            return Response({"error": "api_token is required"})

        payload = {
            "query": """
                query myProfile {
                    myProfile {
                        verifiedPersonalInformation {
                            nationalIdentificationNumber
                        }
                    }
                }
            """,
        }

        try:
            response = requests.post(
                settings.HELSINKI_PROFILE_API_URL,
                json=payload,
                timeout=5,
                verify=True,
                headers={"Authorization": "Bearer " + profile_api_token},
            )
            response.raise_for_status()
        except RequestException:
            return Response({"error": "Error fetching the profile"})

        profile_data = response.json()

        if "errors" in profile_data:
            return Response({"error": "Error fetching the profile"})

        national_identification_number = (
            profile_data.get("data", {})
            .get("myProfile", {})
            .get("verifiedPersonalInformation", {})
            .get("nationalIdentificationNumber")
        )

        century = 0
        if national_identification_number[6] == "+":
            century = 1800
        elif national_identification_number[6] == "-":
            century = 1900
        elif national_identification_number[6] == "A":
            century = 2000

        userdata = self.request.user.userdata

        userdata.birthday = datetime.date(
            year=century + int(national_identification_number[4:6]),
            month=int(national_identification_number[2:4]),
            day=int(national_identification_number[0:2]),
        )
        userdata.save()

        return Response({"birthday": userdata.birthday})
