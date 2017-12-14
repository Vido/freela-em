import re
import time
import datetime
import telegram
import sys, os, django

from django.db import models
from django.db.models.signals import post_save

from decouple import config

from landing_page.models import ClassRequest
from telegram_bot.models import UpdateResponse

chat_id = config('TELEGRAM_CHAT_ID', cast=int)
telegram_api_key = config('TELEGRAM_API_KEY')
bot = telegram.Bot(telegram_api_key)
regex_request_id = re.compile(r'I take him! ClassRequest ID: (\d+)')

def get_username(update_dict):
    _from = update_dict['callback_query']['from']
    if 'username' in _from:
        username = '@' + _from['username']
    elif 'first_name' in _from:
        username = _from['first_name']
    else:
        username = ''
    return username


def send_contact(class_request_obj, user_id, update_dict):
    """
    """
    try:
        msg_str = 'Student %s is avalible for %s minutes. Please contact via %s' % (
                class_request_obj.name,
                class_request_obj.time,
                class_request_obj.preferred_im)
        bot.send_message(chat_id=user_id, text=msg_str)
        bot.sendContact(
                chat_id=user_id,
                phone_number=class_request_obj.phone_number,
                first_name=class_request_obj.name,
                parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        print('Exception', e)
        username = get_username(update_dict)
        help_text = '%s In order to receive the contact click on the bot`s private chat and click "Start"' % username
        bot.send_message(chat_id=chat_id, text=help_text)
        raise

def warn_contact_taken(class_request_obj, user_id, update_dict, last_update_response):
    """
    """

    print('warn_contact_taken() - Disabled')
    return

    try:
        username = get_username(update_dict)
        msg_str = 'Too late! %s was already taken by %s' % (
                class_request_obj.name, username)
        bot.send_message(chat_id=user_id, text=msg_str)

    except Exception as e:
        print('Exception', e)
        username = get_username(update_dict)
        help_text = '%s In order to receive the contact click on the bot`s private chat and click "Start"' % username
        bot.send_message(chat_id=chat_id, text=help_text)

def send_contact_private():

    print('START - send_contact_private()')

    for update in bot.getUpdates():
        dict_update = update.to_dict()
        #print(dict_update)

        if 'callback_query' in dict_update:
            match = regex_request_id.match(dict_update['callback_query']['data'])
            request_id = match.group(1)
            user_id = dict_update['callback_query']['from']['id']

            #print('request_id: ', request_id)
            #print('user_id: ', user_id)
            #print('from:', dict_update['callback_query']['from'])

            class_request_obj = ClassRequest.objects.get(pk=request_id)
            update_response = UpdateResponse.objects.filter(class_request_id=request_id)

            if update_response.exists():
                for update_obj in update_response:
                    print('update_response.exists()')
                    first_taker_id = update_obj.update_dict['callback_query']['from']['id']
                    taker_id = dict_update['callback_query']['from']['id']
                    if not first_taker_id == taker_id:
                        print('warn_contact_taken()')
                        warn_contact_taken(class_request_obj,
                                       user_id,
                                       dict_update,
                                       update_obj)
                    #edit
                    print('Edit')
                    print(update_obj.update_dict)
                    username = get_username(update_obj.update_dict)
                    taken_msg = 'Student %s was avalible for %s minutes... But %s took it.' % (
                            class_request_obj.name, class_request_obj.time, username)
                    message_id=dict_update['callback_query']['message']['message_id']

                    try:
                        bot.editMessageText(chat_id=chat_id, message_id=message_id, text=taken_msg)
                    except Exception as e:
                        print(e)

                    try:
                        bot.editMessageReplyMarkup(chat_id, message_id=message_id, reply_markup=None)
                    except Exception as e:
                        print(e)


            else:
                print('send_contact_private()')
                send_contact(class_request_obj, user_id, dict_update)
                username = get_username(dict_update)

                UpdateResponse.objects.create(
                        class_request_id=class_request_obj.pk,
                        update_dict=dict_update)



def run():
    # Cron
    for i in range(5):
        print('Date now: %s' % datetime.datetime.now())
        send_contact_private()
        time.sleep(10)