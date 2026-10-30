import psycopg2
from psycopg2 import connect


class DBContextMAnager:
    def __init__(self, db_connect: dict):
        self.conn = None
        self.cursor = None
        self.db_connect = db_connect

    def __enter__(self):
        try:
            self.conn = connect(**self.db_connect)
            self.cursor = self.conn.cursor()
            return self.cursor
        except psycopg2.Error as err:
            print(err)
            if self.conn:
                self.conn.close()
                self.conn = None
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type)
            print(exc_val)
        if self.conn:
            try:
                if exc_type:
                    self.conn.rollback()
                else:
                    self.conn.commit()
            finally:
                try:
                    if self.cursor:
                        self.cursor.close()
                finally:
                    self.conn.close()
        return False
