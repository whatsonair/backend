import json
import traceback

import requests
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
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
        if chat['type'] != 'private':
            send_message(to=chat['id'], text="I can only work with private messages at the moment, sorry.")
            return JsonResponse({
                "action": "no",
                "reason": "non-private chat"
            })

        if not text \
                or not text.startswith('/'):
            send_message(to=chat['id'], text="/songonair <song name> - to get notifications about song on air")
            return JsonResponse({
                "action": "no",
                "reason": "command needed"
            })

        if text.startswith('/songonair'):
            query = text.replace('/songonair', '').strip().lower()
            if not query:
                send_message(to=chat['id'],
                             text="/songonair <song name> - to get notifications about song on air")
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
        else:
            send_message(to=chat['id'],
                         text="/songonair <song name> - to get notifications about song on air")
            return JsonResponse({
                "action": "no",
                "reason": "unknown command: '{}'".format(text),
            })
    except Exception as exc:
        # return HttpResponseBadRequest('{}: {}'.format(type(exc).__name__, str(exc)))
        return HttpResponseBadRequest(traceback.format_exc())
