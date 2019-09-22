import importlib
import logging
from base64 import b64encode

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings

from telegrambot.models import NotificationRequest, RadioStation
from telegrambot.views import send_message


log = logging.getLogger('command_notify')


class Command(BaseCommand):
    help = 'Check radio stations and notify telegram users'

    def handle(self, *args, **options):
        if NotificationRequest.objects.count() == 0:
            log.info('No notification requests')

        for station in RadioStation.objects.filter(monitor=True):
            if not station.scrapper:
                continue

            try:
                function_string = station.scrapper
                mod_name, func_name = function_string.rsplit('.', 1)
                mod = importlib.import_module(mod_name)
                check_station = getattr(mod, func_name)
            except Exception as exc:
                log.exception('Exception while trying to import scrapper {} for radio station {}'.format(station.scrapper, station.name))
                continue

            try:
                air = check_station()
            except Exception:
                log.exception('Exception in scrapper code {} for station {}'.format(station.scrapper, station.name))
                continue

            if not air:
                log.warn("{}: {}".format(station.name, air))
                continue

            log.debug("{}: {}".format(station.name, air))

            # TODO: refactor, just store scrap result in DB, use post_save signal to trigger notifications
            for notif_request in NotificationRequest.objects.filter(user__is_active=True):
                try:
                    if notif_request.request_text in air.lower():
                        cache_key = b64encode("{}{}-{}".format(station.name, air, notif_request.user_id).encode('utf-8'))

                        if not cache.get(cache_key):
                            send_message(to=notif_request.user.telegram_chat_id,
                                         text="{radio}: {song}".format(song=air, radio=station.name))
                            cache.set(cache_key, 'notified', settings.PREVENT_NOTIFICATION_REPEAT_TIMEOUT)

                        log.debug(
                            "Notified user: '{user}' about '{song}' playing on radio '{station}', request text: '{request}'".format(
                                user=notif_request.user.telegram_chat_id,
                                song=air,
                                station=station.name,
                                request=notif_request.request_text
                            ))
                except Exception:
                    log.exception("Exception when attempting to notify '{user}' about '{song}' playing on radio '{station}', request text: '{request}'".format(
                                user=notif_request.user.telegram_chat_id,
                                song=air,
                                station=station.name,
                                request=notif_request.request_text
                            ))