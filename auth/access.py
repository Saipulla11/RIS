from functools import wraps

from flask import redirect, request, session, url_for

# Системная диаграмма вариантов использования в виде словаря:
# группа пользователя -> разделы (имена blueprint), к которым у неё есть доступ.
ACCESS = {
    'admin': ['report'],
    'user': ['query'],
}


def login_required(func):
    """Пускает дальше только авторизованного пользователя."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('auth.login'))
    return wrapper


def group_required(func):
    """Проверяет, что группа пользователя имеет доступ к разделу (по словарю ACCESS)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        section = (request.endpoint or '').split('.')[0]
        if section in ACCESS.get(session.get('user_group'), []):
            return func(*args, **kwargs)
        menu_url = url_for('main_menu')
        return (f'<h2>Доступ запрещён</h2>'
                f'<p>Ваша группа не имеет доступа к этому разделу.</p>'
                f'<a href="{menu_url}">В главное меню</a>', 403)
    return wrapper
