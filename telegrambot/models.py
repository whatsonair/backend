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


class Scrapper(models.Model):
    radio = models.ForeignKey(RadioStation, on_delete=models.CASCADE)
    python_path = models.CharField(max_length=1000, blank=False)
    priority = models.IntegerField(unique=True)
    used = models.IntegerField(default=0)
    success = models.IntegerField(default=0)

    def __str__(self):
        return self.python_path

    @property
    def success_rate(self):
        if self.used:
            return "{:.1%}".format(self.success / self.used)
        else:
            return "0%"
