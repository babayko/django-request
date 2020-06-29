import time
from contextlib import contextmanager

from django.db.backends.postgresql.base import DatabaseWrapper as DjangoDatabaseWrapper
from django.db.backends.utils import CursorWrapper as DjangoCursorWrapper
from django.utils.encoding import force_text

from polls.middleware import thread_locals


@contextmanager
def calc_sql_time(sql):
    timestamp = time.monotonic()

    yield

    print(
        f'Продолжительность SQL-запроса {sql} - '
        f'{time.monotonic() - timestamp:.3f} сек.'
    )


def make_safe(s):
    return s.replace('*', '').replace('\\', '').replace('%', '')


class CursorWrapper(DjangoCursorWrapper):
    def execute(self, sql, params=None):
        path = getattr(thread_locals, 'path', '')
        if path:
            path = make_safe(path)
            sql = f'/* {path} */\n{force_text(sql)}\n/* {path} */'

        with calc_sql_time(sql):
            return super().execute(sql, params)


class DatabaseWrapper(DjangoDatabaseWrapper):
    def create_cursor(self, name=None):
        cursor = super().create_cursor(name)
        return CursorWrapper(cursor, self)

