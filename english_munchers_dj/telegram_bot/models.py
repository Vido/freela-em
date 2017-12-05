import telegram

from django.db import models
from django.db.models.signals import post_save

from decouple import config

from landing_page.models import ClassRequest

chat_id = config('TELEGRAM_CHAT_ID', cast=int)
telegram_api_key = config('TELEGRAM_API_KEY')
bot = telegram.Bot(telegram_api_key)

def send_msg_group(sender, instance, created, **kwargs):

    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    if kwargs.get('raw', False):
        # https://code.djangoproject.com/ticket/17880
        return

    if created:
        button_list = [
            telegram.InlineKeyboardButton('Take it!', callback_data='I take him!')
        ]

        reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
        msg_str = 'Student %s is avalible for %s minutes!' % (instance.name, instance.time)
        bot.send_message(chat_id=chat_id, text=msg_str, reply_markup=reply_markup)

post_save.connect(send_msg_group, sender=ClassRequest)

