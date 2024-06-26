import strawberry_django
import strawberry
from strawberry import auto

from . import models


@strawberry_django.type(models.User)
class UserType:
    id: auto
    email: str
    username: str
    is_staff: bool
    is_active: bool
    date_joined: str
    gender: str


@strawberry.type
class LoginResponse:
    success: bool
    token: str
