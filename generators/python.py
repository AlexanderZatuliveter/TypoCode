
from generators.base import BaseGenerator
import random


class PythonGenerator(BaseGenerator):

    python_words = [
        # Keywords
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
        'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
        'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
        'match', 'case',

        # Special Identifiers
        'self', 'cls', '_', '__', 'self.__', 'self._',

        # Common Built-in Functions
        'print', "print('...')", 'len', 'range', 'type', 'int', 'str', 'list', 'dict', 'set', 'tuple', 'float', 'bool',
        'open', 'input', 'sum', 'min', 'max', 'sorted', 'abs', 'round', 'enumerate', 'zip',
        'map', 'filter', 'reduce', 'any', 'all', 'isinstance', 'issubclass', 'date'

        # Common Dunder (Magic) Methods
        '__init__', '__new__', '__str__', '__repr__', '__len__',
        '__call__', '__getitem__', '__setitem__', '__delitem__',
        '__iter__', '__next__', '__enter__', '__exit__',

        # Common Standard Library Modules
        'os', 'sys', 'json', 're', 'datetime', 'math', 'random', 'itertools', 'collections',
        'functools', 'logging', 'threading', 'multiprocessing', 'asyncio', 'pathlib', 'enum', "Enum",

        # Symbols and Operators
        '+', '-', '*', '/', '//', '%', '**', '==', '!=', '<', '>', '<=', '>=',
        '=', '+=', '-=', '*=', '/=', '//=', '%=', '**=', 'and', 'or', 'not',
        '&', '|', '^', '~', '<<', '>>', 'in', 'not in', 'is', 'is not',
        '->',

        # Delimiters
        '(', ')', '()', '[', ']', '[]', '{', '}', '{}', ':', ';', ',', '.', '...', '_', '@',

        # Other
        'while True:', 'number', 'text', 'module', 'attribute', 'library', 'package',

        # Common variable names
        'i', 'j', 'k', 'x', 'y', 'z', 'name', 'age', 'count', 'result',
        'data', 'item', 'value', 'index', 'temp', 'exception', 'ex', 'e'
        'temp_list', 'args', 'kwargs', 'user_input', 'output', 'filename',
        'path', 'url', 'response', 'status', 'message', 'error', 'config',
        'settings', 'file', 'records', 'response_time', 'timestamp', 'start_time',
        'end_time', 'is_valid', 'is_empty', 'buffer', 'length', 'size', 'key',
        'obj', 'obj_list', 'model', 'query', 'connection', 'log', 'undefined',
        'api', 'instance', 'environment', 'env', 'local', 'localhost',

        # Common constant names
        'PI', 'E', 'MAX_INT', 'MIN_INT', 'NULL', 'TRUE', 'FALSE', 'DEFAULT',
        'SUCCESS', 'FAILURE', 'ERROR', 'TIMEOUT', 'MAX_RETRIES', 'MIN_RETRIES',
        'CACHE_TIMEOUT', 'BUFFER_SIZE', 'MAX_LENGTH', 'MIN_LENGTH', 'MAX_SIZE',
        'MIN_SIZE', 'MAX_VALUE', 'MIN_VALUE', 'API_KEY', 'AUTH_TOKEN', 'DB_HOST',
        'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'LOG_LEVEL', 'LOG_FILE',
        'CACHE_LIMIT', 'SESSION_TIMEOUT', 'MAX_CONNECTIONS', 'MIN_CONNECTIONS',
        'MAX_THREADS', 'MIN_THREADS', 'MAX_ATTEMPTS', 'RETRY_INTERVAL',
        'PAGE_SIZE', 'PAGE_LIMIT', 'BUFFER_CAPACITY', 'TIME_FORMAT', 'DATE_FORMAT',
        'HTTP_STATUS_OK', 'HTTP_STATUS_NOT_FOUND', 'HTTP_STATUS_ERROR', 'SALT',
        'ENCRYPTION_KEY', 'MAX_NAME_LENGTH', 'MIN_NAME_LENGTH', 'API_URL',


        # Command line
        'python', 'python --version', 'python --help', 'python -m venv', 'source bin/activate', 'Scripts\\activate', 'pip install', 'pip install --upgrade', 'pip uninstall', 'pip freeze', 'pip list', 'pip show', 'python -m pip install', 'python -m pip list', 'python -m pip freeze', 'python -c', 'python', 'python -m unittest', 'python -m pydoc', 'python -i', 'python -m timeit', 'python -m http.server', 'python -m cProfile', 'python -m pdb', 'python -m venv', 'deactivate', 'python -m venv .', 'python -m pip install --user', 'python -m pip uninstall --yes', 'python setup.py install', 'python setup.py bdist_wheel', 'python -m ensurepip --upgrade', 'python -m venv --clear', 'pip search', 'python -m tarfile', 'python -m socket', 'python -m smtpd -n -c DebuggingServer'

    ]

    def get(self, length: int) -> str:
        for _ in range(1, 10):
            text = self.__get(length)
            if len(text) == length:
                return text
        raise Exception("Cannot get random text.")

    def __get(self, length: int) -> str:
        total_len = -1
        words = []
        while True:
            if total_len >= length:
                break
            max_word_len = length - total_len - 1
            if max_word_len == 0:
                break

            word = self._get_random_word(max_length=max_word_len)
            words.append(word)
            total_len += len(word) + 1  # + 1 space

        return " ".join(words)

    # def get_old(self, length: int) -> str:
    #     result_string = ''
    #     while len(result_string) < length:
    #         max_word_len = length - len(result_string)
    #         if max_word_len == 1:
    #             word = '.'
    #         elif max_word_len > 5:
    #             if result_string:
    #                 result_string += ' '
    #             word = self._get_random_word(max_length=max_word_len + 1)
    #         else:
    #             word = self._get_random_word(min_length=max_word_len, max_length=max_word_len)

    #         result_string += word

    #     return result_string.rstrip()

    def _get_random_word(self, min_length: int = 0, max_length: int = 999):
        right_words = filter(lambda w: len(w) >= min_length and len(w) <= max_length, self.python_words)
        return random.choice(list(right_words))
