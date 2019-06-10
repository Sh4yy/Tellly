from string import ascii_letters, digits
from random import choices
from telegram import Bot
from config import get_config
import spintax
from string import Template
from urllib.parse import quote


def generate_id(length=6):
    """
    generate a random string
    :param length: string length
    :return: random string
    """
    return ''.join(choices(ascii_letters + digits, k=length))


bot = Bot(get_config()['telegram']['token'])


class SocialLink:

    url = None

    def __init__(self, link):
        self.link = link

    def get_link(self):
        text = quote(spintax.spin("Send me anonymous messages {🤫|😋} #tellly"))
        return self.url.substitute(link=self.link, text=text)

    def get_name(self):
        return None


class Twitter(SocialLink):
    url = Template("https://twitter.com/intent/tweet?url=$link&text=$text")

    def get_name(self):
        return "Share to Twitter"


class Telegram(SocialLink):
    url = Template("https://t.me/share/url?text=$text&url=$link")

    def get_name(self):
        return "Share on Telegram"
