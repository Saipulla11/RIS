# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
import sys

if __package__ in (None, ''):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template
from database.select1 import select_list
from psycopg2 import Error

#init - иницализация даннызх
#
#exit - убираетт оставшиеся от пользователя данные

app = Flask(__name__)
with open(os.path.join(os.path.dirname(__file__), '../data/db_config.json'), encoding='utf-8') as f:
    app.config['db_config'] = json.load(f)

@app.route('/', methods=['GET'])
def query_index():
    prod_param = [1]
    _sql = """select prod_name, prod_measure, prod_price from product
                where prod_category = %s"""
    try:
        result = select_list(_sql, prod_param)
    except (Error, ValueError):
        return render_template('err_query.html', error_message='Ошибка обращения к БД. Проверьте настройки подключения')
    if result is not None:
        print(result)
        prod_title = 'Результаты из бд'
        template_name = 'dynamic.html'
        return render_template(template_name, prod_title=prod_title, products=result)
    else:
        return 'результат не получен'


if __name__ == '__main__':
    app.run()
