"""Every API endpoint declares who may call it, with exactly one of the levels in this file:
`permission_classes = [Anyone]`.
"""

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from django.urls import URLPattern, URLResolver
from rest_framework.permissions import AllowAny, BasePermission, IsAdminUser
from rest_framework.request import Request

from api import URL_PREFIX

# For the type only: DRF loads this module while it sets up `rest_framework.views`
if TYPE_CHECKING:
    from rest_framework.views import APIView


class Anyone(AllowAny):
    pass


class Team(BasePermission):
    """A logged-in team. No team can log in yet, so this lets nobody in."""

    def has_permission(self, request: Request, view: "APIView") -> bool:
        return False


class Organizer(IsAdminUser):
    """An organizer, whose Django account has `is_staff` set."""


class NoAccess(BasePermission):
    """The default for an endpoint without a level, so it's closed until it declares one."""

    def has_permission(self, request: Request, view: "APIView") -> bool:
        return False


_LEVELS = (Anyone, Team, Organizer)


def _declares_one_level(view: Callable[..., Any]) -> bool:
    levels = getattr(getattr(view, "cls", None), "permission_classes", [])
    return len(levels) == 1 and levels[0] in _LEVELS


def undeclared_endpoints(
    patterns: Sequence[URLPattern | URLResolver], prefix: str = ""
) -> list[str]:
    """The route of every API endpoint that doesn't declare exactly one level."""
    undeclared = []
    for pattern in patterns:
        route = prefix + str(pattern.pattern)
        if isinstance(pattern, URLResolver):
            undeclared += undeclared_endpoints(pattern.url_patterns, route)
        elif route.startswith(URL_PREFIX) and not _declares_one_level(pattern.callback):
            undeclared.append(route)
    return undeclared
