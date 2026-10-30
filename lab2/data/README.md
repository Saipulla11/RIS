В db_config.json укажите параметры своей PostgreSQL:

- host — адрес сервера (по умолчанию localhost);
- port — порт сервера (по умолчанию 5432);
- dbname — имя базы данных вместо YOUR_DATABASE;
- user — имя пользователя вместо YOUR_USER;
- password — пароль вместо YOUR_PASSWORD.

Запустите seminar2/app2_0.py и откройте http://127.0.0.1:5000.
Введите номер категории, существующей в вашей базе.
В таблице product нужны поля prod_name, prod_measure, prod_price, prod_category.
Для варианта с главным меню запустите seminar3/app3.oy.py.
seminar2/app2.py показывает категорию 1 без формы ввода.

Подключение использует Flask и psycopg2 (пакет psycopg2-binary).
Файлы auth не изменялись и в этих точках входа не подключаются.
Не публикуйте заполненный конфиг с настоящим паролем.
