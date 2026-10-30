from os import path

from flask import Blueprint, render_template, request, url_for

from auth.access import group_required
from database.sql_provider import SQLProvider
from query_bp.module_route import balance_query, call_query, sub_query

blueprint_query = Blueprint('query', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


def _render(res_info, title):
    back_url = url_for('query.request_handler')
    if res_info.status:
        return render_template('result_table.html', title=title, columns=res_info.columns,
                               rows=res_info.result, back_url=back_url)
    return render_template('err_query.html', error_message=res_info.error_message, back_url=back_url)


@blueprint_query.route('/', methods=['GET'])
@group_required
def request_handler():
    return render_template('queries.html')


@blueprint_query.route('/call', methods=['POST'])
@group_required
def call_handler():
    return _render(call_query(request.form, provider), 'Разговоры по callind_id')


@blueprint_query.route('/sub', methods=['POST'])
@group_required
def sub_handler():
    return _render(sub_query(request.form, provider), 'Абонент по номеру телефона')


@blueprint_query.route('/balance', methods=['POST'])
@group_required
def balance_handler():
    return _render(balance_query(request.form, provider), 'Баланс до и после обновления')
