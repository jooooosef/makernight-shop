from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.utils import translation

from api import URL_PREFIX


def english_api(
    get_response: Callable[[HttpRequest], HttpResponse],
) -> Callable[[HttpRequest], HttpResponse]:
    """The API's messages are for developers, so they stay English for every browser language."""

    def middleware(request: HttpRequest) -> HttpResponse:
        if request.path.startswith(f"/{URL_PREFIX}"):
            with translation.override("en"):
                return get_response(request)
        return get_response(request)

    return middleware
