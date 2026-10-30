from os import path
from flask import render_template, Blueprint, request
from database.sql_provider import SQLProvider
from query_bp.module_route import module_route

blueprint_query = Blueprint('query', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


@blueprint_query.route('/', methods=['GET'])
def request_handler():
    return render_template('input_category.html')


@blueprint_query.route('/', methods=['POST'])
def result_handler():
    res_info = module_route(request.form, provider)
    print("res_info.result = ", res_info.result)
    if res_info.status:
        prod_title = 'Результат из БД'
        return render_template('dynamic.html', prod_title=prod_title, products=res_info.result)
    else:
        return render_template('err_query.html', error_message=res_info.error_message)
