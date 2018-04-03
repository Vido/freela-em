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

