from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.access import Anyone


class StatusView(APIView):
    permission_classes = [Anyone]

    def get(self, request: Request) -> Response:
        return Response({"status": "ok"})
