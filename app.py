from flask import Flask
from config import get_config
from mongoengine import connect
from telegram.ext import Updater
from telegram.ext import CommandHandler
from Controllers.TelegramControllers import *


def init_telegram():
    """ initialize telegram """
    updater = Updater(get_config()['telegram']['token'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('about', help))
    dispatcher.add_handler(CommandHandler('link', link))

    return updater


def init_db():
    """ initialize mongodb """
    connect("tellly", host=get_config()['database']['url'].format(
        username=get_config()['database']['user']['username'],
        password=get_config()['database']['user']['password']
    ))


def init_app():
    """ initialize flask app """
    app = Flask(__name__, static_folder="static")
    return app
