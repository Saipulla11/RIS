from os import path

from flask import Blueprint, render_template, request, url_for
from psycopg2 import Error

from auth.access import group_required
from database.select1 import select_table
from database.sql_provider import SQLProvider

blueprint_report = Blueprint('report', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


def _optional_int(raw, label, low, high):
    """Пустое значение означает 'без фильтра' и даёт None."""
    if raw == '':
        return None
    try:
        value = int(raw)
        if value < low or value > high:
            raise ValueError
    except ValueError:
        raise ValueError(f'{label}: введите целое число от {low} до {high} или оставьте поле пустым')
    return value


@blueprint_report.route('/', methods=['GET'])
@group_required
def report_list():
    back_url = url_for('report.report_list')
    year_raw = request.args.get('year', '').strip()
    month_raw = request.args.get('month', '').strip()
    try:
        year = _optional_int(year_raw, 'Год', 1900, 2100)
        month = _optional_int(month_raw, 'Месяц', 1, 12)
    except ValueError as err:
        return render_template('err_query.html', error_message=str(err), back_url=back_url)

    try:
        columns, rows = select_table(provider.get('report.sql'), [year, year, month, month])
    except (Error, ValueError):
        return render_template('err_query.html',
                               error_message='Ошибка обращения к БД. Проверьте настройки подключения',
                               back_url=back_url)
    return render_template('report_list.html', columns=columns, rows=rows, year=year_raw, month=month_raw)
