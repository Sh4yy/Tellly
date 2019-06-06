from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown


from config import get_config
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def hi_command_handler(bot, update):
    print(update)
    print(bot)

    update.message.reply_text("hey there")


updater = Updater(get_config()['telegram']['token'])
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('hi', hi_command_handler))

updater.start_polling()
updater.idle()

"""
/start -> register user in the db | tell the user about the app
/link -> get user's link (tellly.io/<user_id>)
/about 
"""