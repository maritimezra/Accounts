from django.urls import path
from . import views
from strawberry.django.views import GraphQLView

from accounts.schema import schema

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("sign-up", views.sign_up, name="sign_up"),
    path("graphql", GraphQLView.as_view(schema=schema)),
]
