import json
import traceback

from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
from telegrambot.models import User, NotificationRequest


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
            return JsonResponse({
                "action": "no",
                "reason": "non-private chat"
            })

        if not text \
                or not text.startswith('/'):
            return JsonResponse({
                "action": "no",
                "reason": "command needed"
            })

        if text.startswith('/songonair'):
            query = text.replace('/songonair', '').strip().lower()
            if not query:
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
                    return JsonResponse({
                        "action": "no",
                        "reason": "Notification request for song '{}' already exists for the user".format(query)
                    })

                NotificationRequest.objects.create(
                    user=user,
                    request_text=query
                )
            return JsonResponse({
                "action": "NotificationRequest stored",
                "reason": "",
            })
        else:
            return JsonResponse({
                "action": "no",
                "reason": "unknown command: '{}'".format(text),
            })
    except Exception as exc:
        # return HttpResponseBadRequest('{}: {}'.format(type(exc).__name__, str(exc)))
        return HttpResponseBadRequest(traceback.format_exc())
