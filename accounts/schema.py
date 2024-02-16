import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from .managers import UserManager
from . import types


@strawberry.type
class Query:
    @strawberry.field
    def user(self, email: str) -> types.User:
        pass


@strawberry.type
class Mutation:
    @strawberry.field
    def create_user(self, email: str, password: str) -> types.User:
        user = UserManager().create_user(email=email, password=password)
        return user(id=user.pk)


schema = strawberry.Schema(
    query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension]
)
