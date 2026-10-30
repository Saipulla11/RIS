import os


class SQLProvider:
    def __init__(self, file_path):
        self.scripts = {} #инициализируем словарь
        for file in os.listdir(file_path):
            if file.endswith('.sql'):
                with open(os.path.join(file_path, file), encoding='utf-8') as f:
                    _sql = f.read()
                self.scripts[file] = _sql

    def get(self, file):
        _sql = self.scripts[file]
        return _sql
