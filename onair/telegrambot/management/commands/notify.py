from django.core.management.base import BaseCommand, CommandError

import scrappers
from telegrambot.models import NotificationRequest
from telegrambot.views import send_message


class Command(BaseCommand):
    help = 'Check radio stations and notify telegram users'

    def handle(self, *args, **options):
        if NotificationRequest.objects.count() == 0:
            self.stdout.write('No notification requests')

        stations = [scrappers.hit_fm, scrappers.russkoe_radio_ukraina]
        for check_station in stations:
            air = check_station()
            if not air['onair']:
                continue

            for notif_request in NotificationRequest.objects.all():
                if notif_request.request_text in air['onair'].lower():
                    send_message(to=notif_request.user.telegram_chat_id,
                                 text="'{}' is on air on radio '{}'!".format(air['onair'], air['station']))
                    self.stdout.write("Notified user: '{user}' about '{song}' playing on radio '{station}', request text: '{request}'".format(
                        user=notif_request.user.telegram_chat_id,
                        song=air['onair'],
                        station=air['station'],
                        request=notif_request.request_text
                    ))

