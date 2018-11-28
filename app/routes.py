from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, LoginTelegram

from telethon import TelegramClient


@app.route('/')
@app.route('/index_page')
def index():
    return render_template("index.html", title="Index page")


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index_page')
    return render_template("login.html", title="login", form=form)


@app.route('/t_login', methods=["POST"])
def t_login():
    form = LoginTelegram()
    tel_numb = ''
    if form.phone_numb:
        client = TelegramClient("ses", 614719, "fc06672d383206bf1ba342571da5b318")
        client.connect()
        client.send_code_request(form.phone_numb)
        client.disconnect()

        tel_numb = form.phone_numb
    return render_template("login.html", title="login", form=form, tel_numb=tel_numb)


@app.route('/t_submit', methods=["POST"])
def t_submit():
    form = LoginTelegram()
    if form.validate_on_submit():
        client = TelegramClient("ses", 614719, "fc06672d383206bf1ba342571da5b318")
        client.connect()
        myself = client.sign_in(form.phone_numb, form.code)
        client.disconnect()
        flash(f'user: {myself.get_me().username}')
        return redirect('/index_page')
    return render_template("login.html", title="login", form=form)
