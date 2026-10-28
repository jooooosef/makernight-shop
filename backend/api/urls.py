from django.urls import path, re_path

from api.errors import NotFoundView
from api.status import StatusView

urlpatterns = [
    path("v1/status", StatusView.as_view()),
    re_path("", NotFoundView.as_view()),
]
