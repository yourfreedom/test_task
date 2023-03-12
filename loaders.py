from abc import ABC
from abc import abstractmethod
from typing import Generator

from db import SQLDatabase


class ILoader(ABC):
    """Интерфейс загрузчика."""

    @abstractmethod
    def load(self, rows):
        """
        Загрузка данных.

        Args:
            rows: iterable коллекция строк
        """


class TestTaskLoader(ILoader):
    """Загрузчик для тестового задания."""

    def __init__(self, db: SQLDatabase):
        """
        Инициализация.

        Args:
            db: объект взаимодействия с базой данных SQL
        """
        self.db = db

    def _load(self, row: dict):
        """
        Запись строки в таблицу.

        Args:
            row: строка с данными (объект ExcelRow)
        """
        sql = (
            "INSERT INTO test_table (company, fact_Qliq_data1, fact_Qliq_data2, fact_Qoil_data1, fact_Qoil_data2, "
            "forecast_Qliq_data1, forecast_Qliq_data2, forecast_Qoil_data1, forecast_Qoil_data2, date) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        params = tuple(v for k, v in row.values.items() if k != 'id')
        self.db.execute(sql, params)

    def load(self, rows: Generator[dict, None, None]):
        """
        Загрузка данных

        Args:
            rows: генератор строк(объектов ExcelRow)
        """
        for row in rows:
            self._load(row)
