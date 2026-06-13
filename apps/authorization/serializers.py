# apps/authorization/serializers.py

from rest_framework import serializers


class DiscordLoginSerializer(serializers.Serializer):
    code = serializers.CharField()
    redirect_uri = serializers.URLField()
