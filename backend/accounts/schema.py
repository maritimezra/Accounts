import strawberry
from typing import List
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry_jwt_auth.extension import JWTExtension
from strawberry_jwt_auth.decorator import login_required

from .models import User
from .types import UserType


@strawberry.type
class Query:

    @strawberry.field
    # @login_required  # Uncomment to protect the field with authentication
    def me(self, info) -> UserType:
        return info.context.request.user

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

    @strawberry.field
    def get_user_with_phone_number(self, phone_number: str) -> List[UserType]:
        return User.objects.filter(phone_number__iexact=str(phone_number))


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        gender: str,
        phone_number: str,
    ) -> UserType:
        user = User.objects.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number,
        )
        return user

    @strawberry.mutation
    def update_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        gender: str,
        phone_number: str,
    ) -> UserType:
        user = User.objects.get(email=email)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.phone_number = phone_number
        user.save()
        return user

    @strawberry.mutation
    def login(self, info, email: str, password: str) -> bool:
        user = User.objects.get(email=email)

        if user.check_password(password):
            setattr(info.context, "userID", user.id)
            setattr(info.context.request, "issueNewTokens", True)
            setattr(info.context.request, "clientID", user.id)
            return True
        else:
            return False

    @strawberry.mutation
    def logout(self, info) -> bool:
        user = info.context.request.user

        if user:
            setattr(info.context.request, "revokeTokens", True)
            return True
        else:
            return False

    @strawberry.mutation
    @login_required
    def change_password(self, info, old_password: str, new_password: str) -> bool:
        user = info.context.request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return True
        else:
            return False


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
        JWTExtension,
    ],
)
