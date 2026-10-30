from psycopg2 import Error

from database.select1 import select_list


class ResultInfo:
    def __init__(self, status, result=None, error_message=''):
        self.status = status
        self.result = result
        self.error_message = error_message


def module_route(user_input, provider):
    try:
        prod_category = int(user_input.get('prod_category', ''))
        if prod_category < 1 or prod_category > 2147483647:
            raise ValueError
    except (ValueError, TypeError):
        return ResultInfo(False, error_message='Введите целый номер категории от 1 до 2147483647')

    _sql = provider.get('product.sql')
    prod_param = [prod_category]
    try:
        result = select_list(_sql, prod_param)
    except (Error, ValueError):
        return ResultInfo(False, error_message='Ошибка обращения к БД. Проверьте настройки подключения')
    return ResultInfo(True, result=result)
