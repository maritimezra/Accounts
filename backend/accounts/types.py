import strawberry_django
from strawberry import auto

from . import models


@strawberry_django.type(models.User)
class UserType:
    id: auto
    email: str
    first_name: str
    last_name: str
    is_staff: bool
    is_active: bool
    date_joined: str
    gender: str
    phone_number: str
