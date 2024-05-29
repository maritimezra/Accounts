from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from .managers import UserManager


class Gender(models.TextChoices):
    MALE = "M"
    FEMALE = "F"
    NONBINARY = "N"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=1, choices=Gender, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name or self.email.split("@")[0]

    def get_user_with_id(id):
        return User.objects.filter(id=id).first()

    def get_user_with_email(email):
        return User.objects.filter(email=email).first()

    def get_user_with_first_name(first_name):
        return User.objects.filter(first_name=first_name).first()

    def get_user_with_last_name(last_name):
        return User.objects.filter(last_name=last_name).first()

    def get_user_with_phone_number(phone_number):
        return User.objects.filter(phone_number=phone_number).first()
