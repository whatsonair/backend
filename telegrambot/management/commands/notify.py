import importlib
from base64 import b64encode
from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings
from django.db.models import F

from telegrambot.models import NotificationRequest, Scrapper
from telegrambot.views import send_message


class Command(BaseCommand):
    help = 'Check radio stations and notify telegram users'

    def handle(self, *args, **options):
        if NotificationRequest.objects.count() == 0:
            self.stdout.write('No notification requests')

        for scrapper in Scrapper.objects.filter(radio__monitor=True):
            try:
                function_string = scrapper.python_path
                mod_name, func_name = function_string.rsplit('.', 1)
                mod = importlib.import_module(mod_name)
                check_station = getattr(mod, func_name)
            except Exception as exc:
                continue

            air = check_station()
            scrapper.used = F('used') + 1
            scrapper.save()
            self.stdout.write('{} DEBUG {}: {}'.format(datetime.now(), scrapper.radio.name, air))
            if not air:
                continue

            scrapper.refresh_from_db()
            scrapper.success = F('success') + 1
            scrapper.save()

            for notif_request in NotificationRequest.objects.filter(user__is_active=True):
                cache_key = b64encode(
                    "{}{}-{}".format(scrapper.radio.name, air, notif_request.user_id).encode('utf-8'))
                if notif_request.request_text in air.lower() \
                        and not cache.get(cache_key):
                    send_message(to=notif_request.user.telegram_chat_id,
                                 text="{radio}: {song}".format(song=air, radio=scrapper.radio.name))
                    cache.set(cache_key, 'notified', settings.PREVENT_NOTIFICATION_REPEAT_TIMEOUT)

                    self.stdout.write("{ts} DEBUG Notified user: '{user}' about '{song}' playing on radio '{station}', request text: '{request}'".format(
                        ts=datetime.now(),
                        user=notif_request.user.telegram_chat_id,
                        song=air,
                        station=scrapper.radio.name,
                        request=notif_request.request_text
                    ))
