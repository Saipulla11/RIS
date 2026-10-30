import json
import os

from flask import Flask, redirect, render_template, session, url_for

from auth.access import ACCESS, login_required
from auth.route import blueprint_auth
from query_bp.route import blueprint_query
from report_bp.route import blueprint_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-me')

with open(os.path.join(BASE_DIR, 'data', 'db_config.json'), encoding='utf-8') as f:
    app.config['db_config'] = json.load(f)

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_report, url_prefix='/report')


@app.route('/')
@login_required
def main_menu():
    user_group = session['user_group']
    sections = ACCESS.get(user_group, [])
    return render_template('internal_user_menu.html',
                           user_group=user_group,
                           can_query='query' in sections,
                           can_report='report' in sections)


@app.route('/exit')
def exit_func():
    session.clear()
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
