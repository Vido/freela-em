import re
import time
import datetime
import telegram
import sys, os, django


from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from decouple import config

from landing_page.models import ClassRequest
from landing_page.models import ClassInfo
from telegram_bot.models import UpdateResponse
from telegram_bot.utils import build_menu

from .utils import edit_bots_mgs

chat_id = config('TELEGRAM_CHAT_ID', cast=int)
telegram_api_key = config('TELEGRAM_API_KEY')
bot = telegram.Bot(telegram_api_key)

def send_ask_charge(cinfo):
    print('send_ask_charge()')

    if cinfo.q1_sent is not None:
        print('[Ok] send_ask_charge()')
        return

    print('[  ] send_ask_charge()')

    button_list = [
        telegram.InlineKeyboardButton('Yes',
            callback_data='Yes, the class was given! ClassInfo ID: %d' % cinfo.id),
        telegram.InlineKeyboardButton('No',
            callback_data='No, class did not happened! ClassInfo ID: %d' % cinfo.id)
    ]

    reply_markup = telegram.InlineKeyboardMarkup(
            build_menu(button_list, n_cols=2))
    msg_str = 'Hi %s. Did you gave the class to student %s?' % (cinfo.teacher, cinfo.class_request.name)
    bot.send_message(chat_id=cinfo.chat_id, text=msg_str, reply_markup=reply_markup)

    cinfo.q1_sent = timezone.now()
    cinfo.save()

regex_charge_yes = re.compile(r'Yes, the class was given! ClassInfo ID: (\d+)')
regex_charge_no = re.compile(r'No, class did not happened! ClassInfo ID: (\d+)')

def get_charge_response(dict_update):
    print('get_charge_response')
    if 'callback_query' in dict_update:

        yes_match = regex_charge_yes.match(dict_update['callback_query']['data'])
        no_match = regex_charge_no.match(dict_update['callback_query']['data'])
        success = None

        if yes_match is None and no_match is None:
            print('[N/A] get_charge_response')
            return

        try:
            cinfo_id = yes_match.group(1)
            success = True
        except AttributeError as e:
            print('yes_match', yes_match)
            print('[N/A] get_charge_response - YES not found')
            pass
        try:
            cinfo_id = no_match.group(1)
            success = False
        except AttributeError as e:
            print('no_match', no_match,)
            print('[N/A] get_charge_response - NO not found')
            pass
        print('cinfo_id: ', cinfo_id)

        user_id = dict_update['callback_query']['from']['id']
        print('CHARGE callback:', dict_update['callback_query'])
        #print('CHARGE callback from:', dict_update['callback_query']['from'])
        print('user_id: ', user_id)
        print('ClassRequest ID', cinfo_id)

        cinfo_obj = ClassInfo.objects.get(pk=cinfo_id)
        print('success', success if success is not None else 'None')

        if success is not None:
            cinfo_obj.success = success
            cinfo_obj.save()

            #Edit Bot's msg
            #print('** dict_update', dict_update)
            msg_id = dict_update['callback_query']['message']['message_id']
            print('msg_id', msg_id)
            msg_str = 'Hi %s. Did you gave the class to student %s? You anwser: %s' % (
                    cinfo_obj.teacher, cinfo_obj.class_request.name,
                    'YES' if success else 'NO')
            from_id = dict_update['callback_query']['from']['id']
            edit_bots_mgs(bot, from_id, msg_id, msg_str)


def send_ask_why(cinfo):
    print('send_ask_why()')

def send_ask_proof(cinfo):
    print('send_ask_proof()')

NO_DELAY = True

def ask_charge_private():
    # Query time

    qs_cinfo = ClassInfo.objects.filter(q1_sent__isnull=True)

    for cinfo in qs_cinfo:

        class_duration = cinfo.class_request.int_class_time()
        delay = datetime.timedelta(minutes=class_duration+5)
        now = timezone.now()

        if NO_DELAY or (now > cinfo.pvt_send_timestamp + delay):
            send_ask_charge(cinfo)
