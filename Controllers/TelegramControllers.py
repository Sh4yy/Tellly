from telegram import Update
from Models import User, Group
from Lang import get_message
from config import get_config


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
                           group_data.user_name, group_data.title)

    return group


def start(bot, update):
    """ register user / group """

    if is_private_chat(update):
        user = get_user(update, create=True)
        name = user.first_name if user.first_name else user.username
        user.send_message(get_message("start/private", name=name), parse_mode="markdown")

    elif is_public_chat(update):
        _ = get_group(update)
        update.message.reply_text(get_message("start/public"), parse_mode="markdown")


def help(bot, update):

    if is_private_chat(update):
        user = get_user(update, create=True)
        name = user.first_name if user.first_name else user.username
        user.send_message(get_message("about/private", name=name), parse_mode="markdown")

    elif is_public_chat(update):
        _ = get_group(update)
        update.message.reply_text(get_message("about/public"), parse_mode="markdown")


def link(bot, update):
    """ return user's unique link (if in group, refer to private chat) """

    if is_private_chat(update):
        user = get_user(update, create=True)
        name = user.first_name if user.first_name else user.username
        user.send_message(get_message("link/private",
                                      name=name,
                                      link=user.public_url),
                          parse_mode="markdown")

        print(user.get_profile_picture())

    elif is_public_chat(update):
        _ = get_group(update)
        update.message.reply_text(get_message("link/public"), parse_mode="markdown")


def admin(bot, update):
    """ returns server stats to the admin """

    user = get_user(update)
    if user.chat_id != get_config()['telegram']['admin_id']:
        update.message.reply_text("you are not authorized to use this command")
    else:
        user_ct = User.objects.count()
        group_ct = Group.objects.count()

        user.send_message(f"Admin Info:\n\nUsers: {user_ct}\
                          \nGroups: {group_ct}")


def new_message(user, message):
    """
    send a new message to the user
    :param user: user instance
    :param message: received message
    """

    user.send_message(get_message("message", message=message), parse_mode="markdown")


