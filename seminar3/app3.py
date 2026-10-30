import json
import os
import sys

if __package__ in (None, ''):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import render_template, Flask

from query_bp.route import blueprint_query

app = Flask(__name__)

app.register_blueprint(blueprint_query, url_prefix='/query')


with open(os.path.join(os.path.dirname(__file__), '../data/db_config.json'), encoding='utf-8') as f:
    app.config['db_config']=json.load(f)

@app.route('/')
def main_menu():
    return render_template('internal_main_menu.html')

@app.route('/exit')
def exit_func():
    return 'До свидания'


if __name__ == '__main__':
    app.run()
