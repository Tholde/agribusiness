from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .tokens import account_activation_token


# Create your models here.
# class User(AbstractUser, PermissionsMixin):
class User(models.Model):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    username = models.CharField(max_length=255, verbose_name=_("Username"))
    password = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/", blank=True)
    cv = models.FileField(upload_to="documents/", blank=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user.first_name}-passcode"
