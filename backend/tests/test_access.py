import pytest
from api.access import Anyone, Organizer, Team, undeclared_endpoints
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.urls import URLPattern, URLResolver, get_resolver, include, path
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.views import APIView


# Made-up endpoints, because the real app must not have one without exactly one level
class OrganizerView(APIView):
    permission_classes = [Organizer]


class UndeclaredView(APIView):
    def get(self, request: Request) -> Response:
        return Response({"secret": 42})


class DeclaredTwiceView(APIView):
    permission_classes = [Anyone, Team]


def plain_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


# The test marked with `urls(__name__)` uses these routes instead of the real ones
urlpatterns = [path("api/undeclared", UndeclaredView.as_view())]


def test_every_endpoint_of_the_app_declares_its_access() -> None:
    assert undeclared_endpoints(get_resolver().url_patterns) == []


def test_reports_every_api_endpoint_without_exactly_one_level() -> None:
    patterns: list[URLPattern | URLResolver] = [
        path(
            "api/",
            include(
                [
                    path("organizers", OrganizerView.as_view()),
                    path("undeclared", UndeclaredView.as_view()),
                    path("twice", DeclaredTwiceView.as_view()),
                    path("plain", plain_view),
                ]
            ),
        ),
        path("admin/plain", plain_view),
    ]

    assert undeclared_endpoints(patterns) == ["api/undeclared", "api/twice", "api/plain"]


@pytest.mark.django_db
@pytest.mark.urls(__name__)
def test_endpoint_without_a_declaration_lets_nobody_in(
    api: APIClient, django_user_model: type[User]
) -> None:
    anonymous = api.get("/api/undeclared")
    api.force_login(django_user_model.objects.create_user("ada", is_staff=True))
    organizer = api.get("/api/undeclared")

    assert (anonymous.status_code, anonymous.json()["code"]) == (403, "NOT_LOGGED_IN")
    assert (organizer.status_code, organizer.json()["code"]) == (403, "FORBIDDEN")
