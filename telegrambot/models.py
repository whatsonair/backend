import importlib

from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telegram_chat_id = models.BigIntegerField(blank=True, null=True)


class NotificationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_text = models.CharField(max_length=255)


def validate_exists(python_path):
    if not python_path:
        return
    try:
        function_string = python_path
        mod_name, func_name = function_string.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        check_station = getattr(mod, func_name)
    except AttributeError as exc:
        raise ValidationError(str(exc))


class RadioStation(models.Model):
    name = models.CharField(max_length=255, blank=False)
    url = models.URLField()
    monitor = models.BooleanField(default=True)
    scrapper = models.CharField(max_length=1000, null=True, validators=[validate_exists])

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def scrapper_set(self):
        return bool(self.scrapper)


class Playlist(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    station = models.ForeignKey(RadioStation, on_delete=models.PROTECT)
    on_air = models.CharField(max_length=1000, null=True)
