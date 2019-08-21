import json
import textwrap
import traceback

import requests
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
from telegrambot.models import User, NotificationRequest


def send_message(to, text):
    requests.post(
        'https://api.telegram.org/bot{token}/sendMessage'.format(token=settings.TELEGRAM_TOKEN),
        json={
            "chat_id": to,
            "text": text
        }
    )


class Replier:
    def __init__(self, to):
        self.to = to

    def send_supported_commands(self):
        msg = textwrap.dedent("""\
            Hi! :)
            I can send you a message when your favorite songs are on air.
            Just request notification with "/songonair michael jackson billie jean" and I will send notification any time billie jean is on air.
            Cheers.
            
        """)
        send_message(to=self.to,
                     text=msg)

    def send_list_empty(self):
        send_message(to=self.to, text='Нет нотификаций')

    def send_notifications_list(self, notifs):
        if not notifs:
            self.send_list_empty()
            return
        lines = []
        for i, text in enumerate(notifs, 1):
            lines.append("{}. {}".format(i, text))
        send_message(to=self.to, text='\n'.join(lines))


@csrf_exempt
def telegram_webhook(request):
    """
    {
        "update_id": 1372564,
        "message": {
            "message_id": 9,
            "from": {
                "id": 379270420,
                "is_bot": false,
                "first_name": "Yegor",
                "last_name": "Ivashchenko",
                "language_code": "ru"
            },
            "chat": {
                "id": 379270420,
                "first_name": "Yegor",
                "last_name": "Ivashchenko",
                "type": "private"
            },
            "date": 1566217734,
            "text": "Django?"
        }
    }

    {
        "update_id": 1372565,
        "message": {
            "message_id": 10,
            "from": {
                "id": 379270420,
                "is_bot": false,
                "first_name": "Yegor",
                "last_name": "Ivashchenko",
                "language_code": "ru"
            },
            "chat": {
                "id": 379270420,
                "first_name": "Yegor",
                "last_name": "Ivashchenko",
                "type": "private"
            },
            "date": 1566217839,
            "text": "/command example",
            "entities": [
                {
                    "offset": 0,
                    "length": 8,
                    "type": "bot_command"
                }
            ]
        }
    }
    :param request:
    :return:
    """
    # TODO: add to queue for processing later
    try:
        body = json.loads(request.body.decode())

        # TODO: validation?
        message = body.get('message', {})  # Optional. New incoming message of any kind — text, photo, sticker, etc
        text = message.get('text', '')  # Optional. For text messages, the actual UTF-8 text of the message, 0-4096 characters.
        chat = message['chat']
        replier = Replier(to=chat['id'])
        if chat['type'] != 'private':
            send_message(to=chat['id'], text="I can only work with private messages at the moment, sorry.")
            return JsonResponse({
                "action": "no",
                "reason": "non-private chat"
            })

        if not text \
                or not text.startswith('/'):
            replier.send_supported_commands()
            return JsonResponse({
                "action": "no",
                "reason": "command needed"
            })

        if text.startswith('/songonair'):
            query = text.replace('/songonair', '').strip().lower()
            if not query:
                replier.send_supported_commands()
                return JsonResponse({
                    "action": "no",
                    "reason": "<song> parameter is missing"
                })

            with transaction.atomic():
                user, created = User.objects.get_or_create(
                    telegram_chat_id=chat['id'],
                    defaults=dict(
                        username=chat.get('username', chat['id']),
                        first_name=chat.get('first_name', ''),
                        last_name=chat.get('last_name', ''),
                    ),
                )
                if NotificationRequest.objects.filter(user=user, request_text=query):
                    send_message(
                        to=chat['id'],
                        text="I already told you... "
                             "I will notify you when '{}' is on air on one of the supported radio stations".format(query)
                    )
                    return JsonResponse({
                        "action": "no",
                        "reason": "Notification request for song '{}' already exists for the user".format(query)
                    })

                NotificationRequest.objects.create(
                    user=user,
                    request_text=query
                )
            send_message(to=chat['id'],
                         text="I will notify you when '{}' is on air on one of the supported radio stations".format(query))
            return JsonResponse({
                "action": "NotificationRequest stored",
                "reason": "",
            })
        elif text.startswith('/list'):
            user, created = User.objects.get_or_create(
                telegram_chat_id=chat['id'],
                defaults=dict(
                    username=chat.get('username', chat['id']),
                    first_name=chat.get('first_name', ''),
                    last_name=chat.get('last_name', ''),
                ),
            )
            if created:
                replier.send_list_empty()
                replier.send_supported_commands()
                return JsonResponse({
                    "action": "sent empty notifications list",
                    "reason": "no notifications for the user",
                })
            notifs = []
            for notif in NotificationRequest.objects.filter(user=user).order_by('id'):
                notifs.append(notif.request_text)

            replier.send_notifications_list(notifs)
            return JsonResponse({
                "action": "sent notifications list",
                "reason": "",
            })
        else:
            replier.send_supported_commands()
            return JsonResponse({
                "action": "no",
                "reason": "unknown command: '{}'".format(text),
            })
    except Exception as exc:
        # return HttpResponseBadRequest('{}: {}'.format(type(exc).__name__, str(exc)))
        return HttpResponseBadRequest(traceback.format_exc())
