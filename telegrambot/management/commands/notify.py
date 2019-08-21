from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.conf import settings

import scrappers
from telegrambot.models import NotificationRequest
from telegrambot.views import send_message


class Command(BaseCommand):
    help = 'Check radio stations and notify telegram users'

    def handle(self, *args, **options):
        if NotificationRequest.objects.count() == 0:
            self.stdout.write('No notification requests')

        for check_station in scrappers.I_UA:
            air = check_station()
            self.stdout.write('{} DEBUG {}'.format(datetime.now(), air))
            if not air['onair']:
                continue

            for notif_request in NotificationRequest.objects.filter(user__is_active=True):
                cache_key = "{}{}-{}".format(air['station'], air['onair'], notif_request.user_id)
                if notif_request.request_text in air['onair'].lower() \
                        and not cache.get(cache_key):
                    send_message(to=notif_request.user.telegram_chat_id,
                                 text="'{radio}': '{song}'".format(song=air['onair'], radio=air['station']))
                    cache.touch(cache_key, settings.PREVENT_NOTIFICATION_REPEAT_TIMEOUT)
                    self.stdout.write("{ts} DEBUG Notified user: '{user}' about '{song}' playing on radio '{station}', request text: '{request}'".format(
                        ts=datetime.now(),
                        user=notif_request.user.telegram_chat_id,
                        song=air['onair'],
                        station=air['station'],
                        request=notif_request.request_text
                    ))
