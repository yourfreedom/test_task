import os
from abc import ABC, abstractmethod
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


class IDatabase(ABC):
    """Интерфейс базы данных."""

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Выполняет запрос."""

    @abstractmethod
    def close_connection(self):
        """Закрывает соединение с базой."""


class SQLDatabase(IDatabase, ABC):
    """Базы данных поддерживающие язык SQL."""


class PostgresDatabase(SQLDatabase):
    """Класс взаимодействия с базой PostgreSQl."""

    def __init__(self, database, user, password=None, host=None, port=None):
        self._conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def execute(self, sql, params=None):
        """
        Выполняет запрос к базе данных.

        Args:
            sql: строка с описанием запроса
            params: словарь с параметрами
        """
        with self._conn.cursor() as cur:
            if params:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
        self._conn.commit()

    def close_connection(self):
        """Закрывает соединение с базой."""
        self._conn.close()

    def create_tables(self):
        """Создает таблицы описанные в файлике init.sql"""
        sql_file = Path(__file__).resolve().parent / 'sql' / 'init.sql'
        with open(sql_file, 'r') as f:
            sql = f.read()

        self.execute(sql)


load_dotenv()


db = PostgresDatabase(
    database=os.getenv('PG_DB'),
    user=os.getenv('PG_USER'),
    password=os.getenv('PG_PASSWORD'),
    host=os.getenv('PG_HOST'),
    port=os.getenv('PG_PORT'),
)
db.create_tables()
