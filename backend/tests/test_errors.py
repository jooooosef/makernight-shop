import logging
from typing import Any

import pytest
from api.access import Anyone
from api.errors import ApiError, ErrorCode
from django.http import Http404
from django.urls import path
from rest_framework import exceptions, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.views import APIView


# Made-up endpoints that fail in each way, which the real API has no endpoints for.
# The tests marked with `urls(__name__)` use these routes instead of the real ones.
class AddressSerializer(serializers.Serializer[Any]):
    city = serializers.CharField()


class OrderSerializer(serializers.Serializer[Any]):
    quantity = serializers.IntegerField()
    address = AddressSerializer()


class OrdersView(APIView):
    permission_classes = [Anyone]

    def post(self, request: Request) -> Response:
        OrderSerializer(data=request.data).is_valid(raise_exception=True)
        return Response(status=201)


class BrokenView(APIView):
    permission_classes = [Anyone]

    def get(self, request: Request) -> Response:
        raise RuntimeError("the database password is hunter2")


class UnknownApiExceptionView(APIView):
    permission_classes = [Anyone]

    def get(self, request: Request) -> Response:
        raise exceptions.APIException("the database password is hunter2")


class OrderView(APIView):
    permission_classes = [Anyone]

    def get(self, request: Request, number: int) -> Response:
        raise ApiError(404, ErrorCode.NOT_FOUND, f"There is no order {number}.")


class ItemView(APIView):
    permission_classes = [Anyone]

    def get(self, request: Request, number: int) -> Response:
        # As `get_object_or_404` does
        raise Http404


urlpatterns = [
    path("api/orders", OrdersView.as_view()),
    path("api/orders/<int:number>", OrderView.as_view()),
    path("api/items/<int:number>", ItemView.as_view()),
    path("api/broken", BrokenView.as_view()),
    path("api/unknown-api-exception", UnknownApiExceptionView.as_view()),
]


def test_unknown_url_and_wrong_method_get_the_error_body(api: APIClient) -> None:
    unknown_url = api.post("/api/v1/nowhere")
    wrong_method = api.delete("/api/v1/status")

    assert unknown_url.status_code == 404
    assert unknown_url.json() == {
        "code": "NOT_FOUND",
        "message": "This URL doesn't exist.",
        "details": None,
    }
    assert (wrong_method.status_code, wrong_method.json()["code"]) == (405, "METHOD_NOT_ALLOWED")


@pytest.mark.urls(__name__)
def test_api_error_answers_with_its_status_code_and_message(api: APIClient) -> None:
    response = api.get("/api/orders/7")

    assert response.status_code == 404
    assert response.json() == {
        "code": "NOT_FOUND",
        "message": "There is no order 7.",
        "details": None,
    }


@pytest.mark.urls(__name__)
def test_invalid_input_names_every_rejected_field(api: APIClient) -> None:
    response = api.post("/api/orders", {"quantity": "many", "address": {}}, format="json")

    assert response.status_code == 400
    assert response.json() == {
        "code": "INVALID_INPUT",
        "message": "The input is invalid.",
        "details": [
            {"field": "quantity", "message": "A valid integer is required."},
            {"field": "address.city", "message": "This field is required."},
        ],
    }


@pytest.mark.urls(__name__)
def test_body_that_is_not_json_is_invalid_input(api: APIClient) -> None:
    response = api.post("/api/orders", "not json", content_type="application/json")

    assert response.json()["code"] == "INVALID_INPUT"


@pytest.mark.urls(__name__)
@pytest.mark.parametrize("url", ["/api/broken", "/api/unknown-api-exception"])
def test_unexpected_error_is_logged_and_leaks_nothing(
    api: APIClient, caplog: pytest.LogCaptureFixture, url: str
) -> None:
    response = api.get(url)

    assert response.status_code == 500
    assert response.json() == {
        "code": "INTERNAL",
        "message": "An unexpected error occurred.",
        "details": None,
    }
    [record] = [r for r in caplog.records if r.levelno == logging.ERROR and r.exc_info]
    assert "hunter2" in str(record.exc_info)


@pytest.mark.urls(__name__)
def test_djangos_not_found_is_not_found(api: APIClient) -> None:
    response = api.get("/api/items/7")

    assert response.status_code == 404
    assert response.json()["code"] == "NOT_FOUND"


@pytest.mark.urls(__name__)
def test_messages_are_english_even_for_a_german_browser(api: APIClient) -> None:
    response = api.post(
        "/api/orders",
        {"quantity": "many", "address": {"city": "Berlin"}},
        format="json",
        headers={"accept-language": "de-DE,de;q=0.9"},
    )

    assert response.json()["details"] == [
        {"field": "quantity", "message": "A valid integer is required."}
    ]
