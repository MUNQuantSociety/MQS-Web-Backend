# apps/authorization/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.authorization.serializers import DiscordLoginSerializer
from apps.authorization.services.discord import DiscordAPIError
from apps.authorization.services.discord_auth import login_with_discord


class DiscordLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DiscordLoginSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        try:
            result = login_with_discord(
                code=serializer.validated_data["code"],
                redirect_uri=serializer.validated_data["redirect_uri"],
            )

        except DiscordAPIError as error:
            return Response(
                {
                    "success": False,
                    "message": "Discord authentication failed",
                    "error": error.args[0],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "data": result,
            },
            status=status.HTTP_200_OK,
        )
