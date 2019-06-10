from flask import Blueprint, render_template, abort, request, redirect
from Models import User
from Controllers import TelegramControllers

mod = Blueprint("routes", __name__)


@mod.route('/')
def index():
    return redirect('https://t.me/telllybot')


@mod.route('/<public_id>', methods=['GET'])
def message(public_id):

    user = User.get_by_public_id(public_id)
    print(user)
    if not user:
        return abort(404)

    return render_template('message.html', user=user)


@mod.route('/<public_id>/submit', methods=['GET'])
def submit_message(public_id):

    user = User.get_by_public_id(public_id)
    if not user:
        return abort(404)

    message = request.args.get('message')
    if not message or len(message) > 260:
        return abort(400)

    TelegramControllers.new_message(user, message)

    return render_template('success.html', user=user)