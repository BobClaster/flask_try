from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, LoginTelegram

from telethon import TelegramClient
from telethon import sync

@app.route('/')
@app.route('/index_page')
def index():
    return render_template("index.html", title="Index page")


# @app.route('/login', methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for user {}, remember_me={}'.format(
#             form.username.data, form.remember_me.data))
#         return redirect('/index_page')
#     return render_template("login.html", title="login", form=form)


@app.route('/t_login')
def t_login():
    client = TelegramClient("ses", 614719, "fc06672d383206bf1ba342571da5b318")
    client.connect()

    if client.is_user_authorized():
        flash(f'user: {client.get_me().username}')
        client.disconnect()
        return redirect('/index_page')

    form = LoginTelegram()
    return render_template("telegram_login.html", title="login", form=form)


@app.route('/send_code', methods=["POST"])
def send_code():
    client = TelegramClient("ses", 614719, "fc06672d383206bf1ba342571da5b318")
    client.connect()

    if client.is_user_authorized():
        flash(f'user: {client.get_me().username}')
        client.disconnect()
        return redirect('/index_page')

    form = LoginTelegram()
    tel_numb = ''
    if form.phone_numb:
        client = TelegramClient("ses", 614719, "fc06672d383206bf1ba342571da5b318")
        client.connect()
        client.send_code_request(form.phone_numb.data)
        client.disconnect()

        tel_numb = form.phone_numb
    return render_template("telegram_send_code.html", title="login", form=form, tel_numb=tel_numb)


@app.route('/t_submit', methods=["POST"])
def t_submit():
    client = TelegramClient("ses", 614719, "fc06672d383206bf1ba342571da5b318")
    client.connect()

    if client.is_user_authorized():
        flash(f'user: {client.get_me().username}')
        client.disconnect()
        return redirect('/index_page')

    form = LoginTelegram()
    if form.validate_on_submit() and not client.is_user_authorized():
        client.send_code_request(form.phone_numb.data)
        client.sign_in(form.phone_numb.data, form.code.data)

    flash(f'user: {client.get_me().username}')
    client.disconnect()
    return redirect('/index_page')
