from django.db import models
from django.contrib.auth.models import AbstractUser
from home.manager import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=16)
    bio = models.CharField(max_length=150, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
