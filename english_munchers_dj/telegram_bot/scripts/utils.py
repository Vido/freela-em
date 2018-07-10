from landing_page.models import ClassInfo

# TODO: Fallback value
def safeget(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct

def get_cinfo(dict_update):
    teacher_id = safeget(dict_update, 'message', 'from', 'id')
    cinfo_list = ClassInfo.objects.filter(
            q2_sent_msgid__isnull=False, chat_id=teacher_id).exclude(
            q2_sent_msgid=0)
    cinfo_obj = cinfo_list.last()

    return cinfo_obj

def edit_bots_mgs(bot, chat_id, message_id, new_text):

    try:
        # Remove bottons
        bot.editMessageReplyMarkup(chat_id=chat_id, message_id=message_id, reply_markup=None)
    except Exception as e:
        print('edit_bots_mgs - Remove bottons failed')
        #raise
        print(e)

    try:
        # Change txt
        bot.editMessageText(chat_id=chat_id, message_id=message_id, text=new_text)
    except Exception as e:
        print('edit_bots_mgs - Change txt failed')
        #raise
        print(e)

