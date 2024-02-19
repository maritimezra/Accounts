import strawberry
import strawberry_django
from typing import List
from strawberry_django.optimizer import DjangoOptimizerExtension

from .models import User
from .types import UserType


@strawberry.type
class Query:
    @strawberry.field
    def get_users(self) -> List[UserType]:
        return User.objects.all()

    @strawberry.field
    def get_user_with_id(self, id: str) -> List[UserType]:
        return User.objects.filter(id=id)

    @strawberry.field
    def get_user_with_email(self, email: str) -> List[UserType]:
        return User.objects.filter(email=email)

    @strawberry.field
    def get_user_with_first_name(self, first_name: str) -> List[UserType]:
        return User.objects.filter(first_name=first_name)

    @strawberry.field
    def get_user_with_last_name(self, last_name: str) -> List[UserType]:
        return User.objects.filter(last_name=last_name)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, email: str, first_name: str, last_name: str) -> UserType:
        user = User.objects.create(
            email=email, first_name=first_name, last_name=last_name
        )
        return user

    @strawberry.mutation
    def update_user(self, email: str, first_name: str, last_name: str) -> UserType:
        user = User.objects.get(email=email)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
