from django.contrib import admin
from django.urls import path, include

from strawberry.django.views import GraphQLView

from accounts.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("django.contrib.auth.urls")),
    path("graphql", GraphQLView.as_view(schema=schema)),
]
