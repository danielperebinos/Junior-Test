from django.contrib import admin
from django.urls import path, include

from apps.users.helper import schema_view

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('admin/', admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("", include("apps.products.urls")),
]
