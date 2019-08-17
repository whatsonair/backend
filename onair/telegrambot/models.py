from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telegram_chat_id = models.BigIntegerField(blank=True, null=True)