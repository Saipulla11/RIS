from os import path

from flask import Blueprint, redirect, render_template, request, session, url_for
from psycopg2 import Error

from database.select1 import select_list
from database.sql_provider import SQLProvider

blueprint_auth = Blueprint('auth', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error_message='')

    user_login = request.form.get('login', '').strip()
    user_password = request.form.get('password', '')
    if not user_login or not user_password:
        return render_template('login.html', error_message='Введите логин и пароль')

    try:
        rows = select_list(provider.get('internal_user.sql'), [user_login, user_password])
    except (Error, ValueError):
        return render_template('login.html',
                               error_message='Ошибка обращения к БД. Проверьте настройки подключения')

    if not rows:
        return render_template('login.html', error_message='Неверный логин или пароль')

    user_id, user_group = rows[0]
    session.clear()
    session['user_id'] = user_id
    session['user_group'] = str(user_group).strip()
    return redirect(url_for('main_menu'))
