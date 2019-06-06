from mongoengine import *
from utilities import generate_id, bot
from config import get_config
from time import time


class User(Document):

    public_id = StringField(unique=True, null=False)
    chat_id = StringField(unique=True, null=False)
    is_bot = BooleanField()
    first_name = StringField()
    last_name = StringField()
    username = StringField(unique=True, null=True)
    reg_date = FloatField(default=time)

    @classmethod
    def register(cls, chat_id, first_name, last_name, username, is_bot=False):
        """
        register a new user on the db
        :param chat_id: user's chat id
        :param first_name: user's first name
        :param last_name: user's last name
        :param username: user's username
        :param is_bot: whether the user is a telegram bot
        :return: User
        """
        user = cls()
        user.chat_id = chat_id
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.is_bot = is_bot
        user.public_id = generate_id(length=6)
        user.save()
        return user

    def send_message(self, text, **kwargs):
        """
        send a message to this user
        :param text: message's text
        :return: the sent message
        """
        return bot.send_message(chat_id=self.chat_id, text=text, **kwargs)

    @classmethod
    def get_user_by_chat_id(cls, chat_id):
        """
        query user by their chat_id
        :param chat_id: target chat id
        :return: User if found else None
        """
        cls.objects(chat_id=chat_id).first()

    @classmethod
    def get_user_by_public_id(cls, public_id):
        """
        query user by their public id
        :param public_id: target public id
        :return: User if found else None
        """
        cls.objects(public_id=public_id).first()

    @property
    def public_url(self):
        """ get user's public url """
        return get_config()['telegram']['user_url'].format(public_id=self.public_id)

    def __str__(self):
        return f"<User(chat_id={self.chat_id}, public_id={self.public_id})>"


class Group(Document):

    chat_id = StringField(unique=True, null=False)
    title = StringField()
    username = StringField(unique=True, null=True)
    type = StringField()
    reg_date = FloatField(default=time)

    @classmethod
    def register(cls, chat_id, type, username, title):
        """
        register a new group
        :param chat_id: group's chat id
        :param type: group's type
        :param username: group's username (optional)
        :param title: group's title (optional)
        :return:
        """
        group = cls()
        group.chat_id = chat_id
        group.title = title
        group.username = username
        group.type = type
        group.save()
        return group

    def send_message(self, text, **kwargs):
        """
        send a message to this user
        :param text: message's text
        :return: the sent message
        """
        return bot.send_message(chat_id=self.chat_id, text=text, **kwargs)


class Feedback(Document):

    text = StringField()
    sent_date = FloatField(default=time)
    target = ReferenceField(User)

    @classmethod
    def new(cls, text, target: User):
        """
        create a new feedback item
        :param text: feedback's text
        :param target: target user instance
        :return: feedback item
        """

        feedback = cls()
        feedback.text = text
        feedback.target = target
        feedback.save()
        return feedback
