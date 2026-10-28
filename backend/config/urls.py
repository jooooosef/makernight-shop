from django.contrib import admin
from django.urls import path

admin.site.site_header = "Maker night shop"
admin.site.site_title = "Maker night shop"

urlpatterns = [
    path("admin/", admin.site.urls),
]
