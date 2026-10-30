from database.DBcm import DBContextMAnager
from flask import current_app


def select_list(_sql, user_list: list) -> list:
    with DBContextMAnager(current_app.config['db_config']) as cursor:
        result = None
        if cursor is None:
            raise ValueError('Курсор не создан') #raise value error
        else:
            cursor.execute(_sql, user_list)
            result = cursor.fetchall()
    return result

def select_dict(_sql, user_dict: dict) -> list:
    user_list = []
    for key in user_dict:
        user_list.append(user_dict[key])
    result = select_list(_sql, user_list)
    return result
