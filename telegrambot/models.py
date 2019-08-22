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


class RadioStation(models.Model):
    name = models.CharField(max_length=255, blank=False)
    url = models.URLField()
    monitor = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def n_scrappers(self):
        return str(self.scrapper_set.count())


def validate_exists(python_path):
    try:
        function_string = python_path
        mod_name, func_name = function_string.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        check_station = getattr(mod, func_name)
    except AttributeError as exc:
        raise ValidationError(str(exc))


class Scrapper(models.Model):
    radio = models.ForeignKey(RadioStation, on_delete=models.CASCADE)
    python_path = models.CharField(max_length=1000, blank=False, validators=[validate_exists])
    used = models.IntegerField(default=0)
    success = models.IntegerField(default=0)

    class Meta:
        unique_together = ('radio', 'python_path')

    def __str__(self):
        return self.python_path

    @property
    def success_rate(self):
        if self.used:
            return "{:.1%}".format(self.success / self.used)
        else:
            return "0%"
