import strawberry
import jwt
from typing import List
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry_jwt_auth.extension import JWTExtension
from strawberry_jwt_auth.decorator import login_required

from .models import User
from .types import UserType, LoginResponse

from django.contrib.auth import authenticate
from django.conf import settings


@strawberry.type
class Query:

    @strawberry.field
    @login_required
    def me(self, info) -> UserType:
        return info.context.request.user

    @strawberry.field
    def get_users(self) -> List[UserType]:
        return User.objects.all()

    # @strawberry.field
    # def get_username(self, info) -> str:
    #     return info.context.request.user.username

    @strawberry.field
    def get_username(self, info) -> UserType:
        auth_header = info.context.request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            raise Exception("Invalid Authorization header format.")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload["user_id"]
            user = User.objects.get(id=user_id)
            return UserType(
                id=user.id,
                username=user.username,
                email=user.email,
                is_staff=user.is_staff,
                is_active=user.is_active,
                gender=user.gender,
                date_joined=user.date_joined,
            )
        except jwt.ExpiredSignatureError:
            print("JWT token has expired")
        except jwt.InvalidTokenError:
            print("Invalid JWT token")

        return None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(
        email: str,
        password: str,
        gender: str,
        username: str,
    ) -> UserType:
        user = User.objects.create_user(
            email=email,
            password=password,
            gender=gender,
            username=username,
        )
        return user

    @strawberry.mutation
    def login(self, info, email: str, password: str) -> LoginResponse:
        user = authenticate(email=email, password=password)

        if user is not None and user.is_authenticated:
            print(f"Authenticated user: {user.email}")
            setattr(info.context.request, "user", user)

            token_payload = {
                "user_id": user.id,
                "email": user.email,
            }
            token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm="HS256")

            return LoginResponse(success=True, token=token)
        else:
            print("Authentication failed")
            return LoginResponse(success=False, token=None)

    @strawberry.mutation
    def logout(self, info) -> bool:
        user = info.context.request.user

        if user:
            setattr(info.context.request, "revokeTokens", True)
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
