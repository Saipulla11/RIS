from datetime import date

from psycopg2 import Error

from database.select1 import select_table


class ResultInfo:
    def __init__(self, status, columns=None, result=None, error_message=''):
        self.status = status
        self.columns = columns
        self.result = result
        self.error_message = error_message


def _int_field(form, name, label):
    try:
        value = int(form.get(name, '').strip())
        if value < 1 or value > 2147483647:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError(f'{label}: введите целое число от 1 до 2147483647')
    return value


def _run(provider, sql_name, params):
    try:
        columns, rows = select_table(provider.get(sql_name), params)
    except (Error, ValueError):
        return ResultInfo(False, error_message='Ошибка обращения к БД. Проверьте настройки подключения')
    return ResultInfo(True, columns=columns, result=rows)


def call_query(form, provider):
    """start и volume по callind_id из таблицы conversation."""
    try:
        callind_id = _int_field(form, 'callind_id', 'callind_id')
    except ValueError as err:
        return ResultInfo(False, error_message=str(err))
    return _run(provider, 'call.sql', [callind_id])


def sub_query(form, provider):
    """Полная строка таблицы sub по phone_number."""
    phone_number = form.get('phone_number', '').strip()
    if not phone_number:
        return ResultInfo(False, error_message='Введите номер телефона')
    return _run(provider, 'sub.sql', [phone_number])


def balance_query(form, provider):
    """old_balance и new_balance из balance_update по sub_id и дате обновления."""
    try:
        sub_id = _int_field(form, 'sub_id', 'sub_id')
        update_date = date.fromisoformat(form.get('update_date', '').strip())
    except ValueError as err:
        message = str(err)
        if 'sub_id' not in message:
            message = 'Укажите дату обновления баланса'
        return ResultInfo(False, error_message=message)
    return _run(provider, 'balance.sql', [sub_id, update_date.isoformat()])
