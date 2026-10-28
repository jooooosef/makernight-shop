from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.access import Anyone


class StatusSerializer(serializers.Serializer[Any]):
    status = serializers.ChoiceField(choices=["ok"], help_text="The server is running.")


class StatusView(APIView):
    permission_classes = [Anyone]

    @extend_schema(responses=StatusSerializer)
    def get(self, request: Request) -> Response:
        return Response(StatusSerializer({"status": "ok"}).data)
