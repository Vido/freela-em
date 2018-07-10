import re
import time
import datetime
import telegram
import sys, os, django

from django.conf import settings
from django.utils import timezone
from decouple import config

from telegram_bot.models import UpdateResponse
from landing_page.models import ClassRequest
from landing_page.models import ClassInfo
from .utils import safeget
from .utils import get_cinfo


chat_id = config('TELEGRAM_CHAT_ID', cast=int)
telegram_api_key = config('TELEGRAM_API_KEY')
bot = telegram.Bot(telegram_api_key)


def get_proof_response(dict_update):
    print('get_response')

    msgid = safeget(dict_update, 'message', 'reply_to_message', 'message_id')
    teacher_id = safeget(dict_update, 'message', 'from', 'id')
    cinfo_obj = get_cinfo(dict_update)

    if msgid is not None:
        original = UpdateResponse.objects.filter(
                class_info_id=cinfo_obj.pk)
                #update_dict__message__message_id=msgid)

        if cinfo_obj.reason_why:
            print('get_response - reason_why. Found')
            return

        if bool(cinfo_obj.proof):
            print('get_response - proof. Found')
            return

        if not cinfo_obj.success:
            cinfo_obj.reason_why = safeget(dict_update, 'message', 'text')
            cinfo_obj.save()
            msg_str = 'Ok! Keep calm and carry on...'

            # send msg
            data = bot.send_message(chat_id=cinfo_obj.chat_id, text=msg_str)

        else:
            try:
                proof_msg = dict_update['message']

                if proof_msg['photo']:
                    # TODO: -1 pega o maior arquivo
                    telegram_file= bot.get_file(
                            proof_msg['photo'][-1]['file_id'])
                elif proof_msg['document']:
                    telegram_file= bot.get_file(
                            proof_msg['document']['file_id'])
                else:
                    raise Exception("Proof not found")

            except Exception as e:
                #IndexError: list index out of range
                print(e)
                return

            basefile = os.path.basename(telegram_file.file_path)
            rel_path = os.path.join('proof', basefile)
            download_path = os.path.join(settings.MEDIA_ROOT, rel_path)
            telegram_file.download(download_path)
            cinfo_obj.proof.name = rel_path
            cinfo_obj.save()

            print('################################ - send_ask_lenght')
            # class_lengh -> only if class was success
            from .confirm_class import send_ask_lenght
            send_ask_lenght(cinfo_obj, chat_id)

            # TUDO pode dar problema
            #msg_str = 'Great! I will analyze it soon.'


def get_classlength_response(dict_update):

    print('get_classlength_response')
    msgid = safeget(dict_update, 'message', 'reply_to_message', 'message_id')
    cinfo_obj = get_cinfo(dict_update)

    if cinfo_obj is None:
        print('[cinfo] get_classlength_response -> is None')
        return

    reply_msg = safeget(dict_update, 'message', 'reply_to_message', 'text')
    if not 'How long did' in reply_msg:
        print('get_proof_response - Wrong msg')
        return

    if cinfo_obj.q3_sent is None:
        print('[Q3] get_classlength_response -> Q3 not sent')
        return

    if msgid is not None:
        if not cinfo_obj.class_length:
            cinfo_obj.class_length = safeget(dict_update, 'message', 'text')
            cinfo_obj.save()
            msg_str = 'Great! I will analyze it soon.'
            data = bot.send_message(chat_id=cinfo_obj.chat_id, text=msg_str)
