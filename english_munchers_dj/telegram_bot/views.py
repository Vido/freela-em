from decouple import config

from django.shortcuts import render
from landing_page.models import ClassRequest

chat_id = config('TELEGRAM_CHAT_ID', cast=int)
telegram_api_key = config('TELEGRAM_API_KEY')
bot = telegram.Bot(telegram_api_key)

def send_msg_group(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        # https://code.djangoproject.com/ticket/17880
        return

    if created:
        button_list = [
            telegram.InlineKeyboardButton('Take it!', callback_data='I take him!')
        ]

        reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
        msg_str = 'Student %s is avalible for %s minutes!' % (name, minutes)
        bot.send_message(chat_id=chat_id, text=msg_str, reply_markup=reply_markup)

post_save.connect(send_msg_group, sender=ClassRequest)

def send_contact_private():
    for update in bot.getUpdates():
        dict_update = update.to_dict()
        if 'callback_query' in dict_update:
            user_id = dict_update['callback_query']['from']['id']
            try:
                bot.sendContact(chat_id=user_id, phone_number=phone, first_name=name,
                    parse_mode="Markdown", disable_web_page_preview=True)
            except Exception as e:
                print(e)
                help_text = '@%s In order to receive the contact click on the bot`s private chat and click "Start"'% dict_update['callback_query']['from']['username']
                bot.send_message(chat_id=chat_id, text=help_text)

if __name__ == '__main__':
    # Cron
    send_contact_private()
