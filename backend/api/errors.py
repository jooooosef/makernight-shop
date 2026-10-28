"""Every API error answers with the same body: a fixed code, a message for developers, and
the rejected fields when the input is invalid.
"""

import logging
from enum import StrEnum
from typing import Any, NoReturn

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView, set_rollback

from api.access import Anyone

logger = logging.getLogger(__name__)


class ErrorCode(StrEnum):
    INVALID_INPUT = "INVALID_INPUT"
    NOT_LOGGED_IN = "NOT_LOGGED_IN"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
    INTERNAL = "INTERNAL"


class FieldErrorSerializer(serializers.Serializer[Any]):
    field = serializers.CharField(
        help_text="The rejected field. A nested field has a dot between the levels."
    )
    message = serializers.CharField(help_text="Why the value was rejected.")


class ErrorBodySerializer(serializers.Serializer[Any]):
    code = serializers.ChoiceField(
        choices=list(ErrorCode), help_text="What went wrong, as a fixed value to branch on."
    )
    message = serializers.CharField(
        help_text="What went wrong, in English. For developers: the page shows its own text."
    )
    details = FieldErrorSerializer(
        many=True,
        allow_null=True,
        help_text="The rejected fields when `code` is `INVALID_INPUT`. Null when no single field "
        "was rejected, such as for a body that isn't JSON.",
    )


class ApiError(exceptions.APIException):
    """Raised by a view to answer with an error code of the shop's own."""

    def __init__(self, status_code: int, code: ErrorCode, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = code


def _code(exc: exceptions.APIException) -> ErrorCode | None:
    """The code for an exception that views and DRF raise on purpose, None for any other."""
    match exc:
        case ApiError():
            return exc.error_code
        case (
            exceptions.ParseError() | exceptions.UnsupportedMediaType() | exceptions.NotAcceptable()
        ):
            return ErrorCode.INVALID_INPUT
        case exceptions.NotAuthenticated() | exceptions.AuthenticationFailed():
            return ErrorCode.NOT_LOGGED_IN
        case exceptions.PermissionDenied():
            return ErrorCode.FORBIDDEN
        case exceptions.NotFound():
            return ErrorCode.NOT_FOUND
        case exceptions.MethodNotAllowed():
            return ErrorCode.METHOD_NOT_ALLOWED
        case _:
            return None


def _field_errors(detail: Any, field: str = "") -> list[dict[str, str]]:
    """One entry per message in DRF's nested errors. A nested field is named like `address.city`."""
    if isinstance(detail, dict):
        return [
            error
            for key, value in detail.items()
            for error in _field_errors(value, f"{field}.{key}" if field else key)
        ]
    if isinstance(detail, list):
        return [error for item in detail for error in _field_errors(item, field)]
    return [{"field": field, "message": str(detail)}]


def _response(
    status: int, code: ErrorCode, message: str, details: list[dict[str, str]] | None = None
) -> Response:
    return Response({"code": code, "message": message, "details": details}, status=status)


def handle_exception(exc: Exception, context: dict[str, Any]) -> Response:
    """DRF's `EXCEPTION_HANDLER`: turns every exception a view raises into the error body."""
    # Rolls back the transaction of the request, as DRF's own handler does
    set_rollback()
    # Django's own, which DRF's handler converts too
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()
    if isinstance(exc, exceptions.ValidationError):
        details = _field_errors(exc.detail)
        return _response(400, ErrorCode.INVALID_INPUT, "The input is invalid.", details)
    if isinstance(exc, exceptions.APIException) and (code := _code(exc)) is not None:
        return _response(exc.status_code, code, str(exc.detail))
    request = context["request"]
    logger.error("Unexpected error in %s %s", request.method, request.path, exc_info=exc)
    return _response(500, ErrorCode.INTERNAL, "An unexpected error occurred.")


class NotFoundView(APIView):
    """Answers every URL under /api/ that no other route matches."""

    permission_classes = [Anyone]
    # Every method ends in `http_method_not_allowed`
    http_method_names: list[str] = []

    def http_method_not_allowed(self, request: HttpRequest, *args: Any, **kwargs: Any) -> NoReturn:
        raise exceptions.NotFound("This URL doesn't exist.")
