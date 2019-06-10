from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from Models import User, Group, Feedback
from Lang import get_message
from config import get_config
from utilities import Twitter, Telegram


def break_msg(message):
    return message.split('**')


def is_private_chat(update: Update):
    """ if the chat is private to a user """
    return update.effective_chat.id > 0


def is_public_chat(update):
    """ if chat is a public chat i.e group/super group etc"""
    return not is_private_chat(update)


def get_user(update: Update, create=True):
    """
    get user from update
    :param update: update instance
    :param create: if set to true, will create user in db
    :return: User
    """

    user_data = update.message.from_user
    user = User.get_by_chat_id(user_data.id)
    if user:
        return user

    user = User.register(user_data.id, user_data.first_name,
                         user_data.last_name, user_data.username,
                         user_data.is_bot, save=create)
    return user


def get_group(update: Update):
    """
    get group from update
    :param update: update instance
    :return: Group
    """

    group_data = update.effective_chat
    group = Group.get_by_chat_id(group_data.id)
    if group:
        return group

    group = Group.register(group_data.id, group_data.type,
                           group_data.username, group_data.title)

    return group


def start(bot, update):
    """ register user / group """

    if is_private_chat(update):
        user = get_user(update, create=True)
        name = user.first_name if user.first_name else user.username

        # create buttons
        buttons = [[get_config()['telegram']['btn']['link'],
                    get_config()['telegram']['btn']['help']]]
        markup = ReplyKeyboardMarkup(buttons)
        msgs = break_msg((get_message("start/private", name=name)))

        for msg in msgs:
            user.send_message(msg, reply_markup=markup, parse_mode="html")

    elif is_public_chat(update):
        _ = get_group(update)
        user = get_user(update, create=False)
        msgs = break_msg(get_message("start/public", name=user.get_name()))

        for msg in msgs[:-1]:
            update.message.reply_text(msg, parse_mode="html")
        update.message.reply_text(msgs[-1], reply_markup=create_start_bot(), parse_mode="html")


def help(bot, update):

    if is_private_chat(update):
        user = get_user(update, create=True)
        name = user.first_name if user.first_name else user.username
        msgs = break_msg(get_message("about/private", name=name))

        for msg in msgs:
            user.send_message(msg, parse_mode="html")

    elif is_public_chat(update):
        _ = get_group(update)
        user = get_user(update, create=False)
        msgs = break_msg(get_message("about/public", name=user.get_name()))

        for msg in msgs[:-1]:
            update.message.reply_text(msg, parse_mode="html")
        update.message.reply_text(msgs[-1],
                                  reply_markup=create_start_bot('Start Tellly Bot'),
                                  parse_mode="html")


def link(bot, update):
    """ return user's unique link (if in group, refer to private chat) """

    if is_private_chat(update):
        user = get_user(update, create=True)
        name = user.first_name if user.first_name else user.username

        telegram_link = Telegram(user.public_url)
        twitter_link = Twitter(user.public_url)

        telegram_btn = InlineKeyboardButton(telegram_link.get_name(), url=telegram_link.get_link())
        twitter_btn = InlineKeyboardButton(twitter_link.get_name(), url=twitter_link.get_link())
        open_btn = InlineKeyboardButton("Open link", url=user.public_url)
        markup = InlineKeyboardMarkup([[telegram_btn, twitter_btn], [open_btn]])

        user.send_message(get_message("link/private",
                                      name=name,
                                      link=user.public_url),
                          reply_markup=markup,
                          parse_mode="html")

    elif is_public_chat(update):
        _ = get_group(update)
        user = get_user(update, create=False)
        update.message.reply_text(get_message("link/public", name=user.get_name()),
                                  reply_markup=create_start_bot('Get your link'), parse_mode="html")


def admin(bot, update):
    """ returns server stats to the admin """

    user = get_user(update)
    if user.chat_id != get_config()['telegram']['admin_id']:
        update.message.reply_text("you are not authorized to use this command")
    else:
        user_ct = User.objects.count()
        group_ct = Group.objects.count()
        feedback_ct = Feedback.objects.count()

        user.send_message(f"Admin Info:\n\nUsers: {user_ct}\
                          \nGroups: {group_ct}\nFeedback: {feedback_ct}")


def new_message(user, message):
    """
    send a new message to the user
    :param user: user instance
    :param message: received message
    """

    Feedback.new(message, user)
    msgs = break_msg(get_message("message", name=user.get_name(), message=message))
    for msg in msgs:
        user.send_message(msg, parse_mode="markdown")


def create_start_bot(btn_text=None):

    tellly = InlineKeyboardButton(btn_text or "Start using Tellly", url='t.me/Telllybot')
    keyboard = InlineKeyboardMarkup([[tellly]])
    return keyboard

