from typing import Any

from drf_spectacular import openapi

from api.errors import ErrorBodySerializer


class AutoSchema(openapi.AutoSchema):
    """Gives every endpoint the error body as its default response, so the API description
    lists every error code.
    """

    # Private in drf-spectacular, but the only method that sees every endpoint's responses,
    # including those set with `@extend_schema`
    def _get_response_bodies(self, direction: Any = "response") -> dict[str, Any]:
        responses = super()._get_response_bodies(direction)
        responses["default"] = self._get_response_for_code(  # type: ignore[no-untyped-call]
            ErrorBodySerializer, "default", direction=direction
        )
        return responses
