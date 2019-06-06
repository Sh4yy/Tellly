from string import ascii_letters, digits
from random import choices
from telegram import Bot
from config import get_config


def generate_id(length=6):
    """
    generate a random string
    :param length: string length
    :return: random string
    """
    return ''.join(choices(ascii_letters + digits, k=length))


bot = Bot(get_config()['telegram']['token'])
