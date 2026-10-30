import json
import os
import sys

if __package__ in (None, ''):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request

from database.sql_provider import SQLProvider
from query_bp.module_route import module_route

app = Flask(__name__)
with open(os.path.join(os.path.dirname(__file__), '../data/db_config.json'), encoding='utf-8') as f:
    app.config['db_config'] = json.load(f)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@app.route('/', methods=['GET', 'POST'])
def query_index():
    if request.method == 'GET':
        return render_template('input_category.html')
    res_info = module_route(request.form, provider)
    if res_info.status:
        prod_title = 'Результат из БД'
        return render_template('dynamic.html', prod_title=prod_title, products=res_info.result)
    else:
        return render_template('err_query.html', error_message=res_info.error_message)


if __name__ == '__main__':
    app.run()
