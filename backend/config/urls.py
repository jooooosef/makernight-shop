from django.contrib import admin
from django.urls import include, path

from api import URL_PREFIX

admin.site.site_header = "Maker night shop"
admin.site.site_title = "Maker night shop"

urlpatterns = [
    path("admin/", admin.site.urls),
    # The language switch in the admin
    path("i18n/", include("django.conf.urls.i18n")),
    path(URL_PREFIX, include("api.urls")),
]
