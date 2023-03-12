import random
from abc import ABC, abstractmethod

from xlrd import open_workbook

from utils import ALL_DATES_IN_MONTH


class Row:
    """Строка данных."""

    def __init__(self):
        self.row_number = None
        self.values = None

    def __str__(self):
        return f'Строка {self.row_number}'


class ExcelRow(Row):
    """Строка данных при импорте из Excel."""

    def __init__(self):
        super().__init__()
        self.sheet_name = None

    def __str__(self):
        return f'{self.sheet_name}, {super().__str__()}'


class IParser(ABC):
    """Интерфейс парсера."""

    row_cls = None

    @abstractmethod
    def get_rows(self):
        """Возвращает коллекцию строк."""


class ExcelParser(IParser):
    """Парсер файлов Excel."""

    row_cls = ExcelRow

    def __init__(self, file_path, skip_rows=None, skip_sheets=None):
        """
        Инициализация объекта

        Args:
            file_path: str путь к файлу
            skip_rows: tuple с номерами строк, которые нужно пропустить
            skip_sheets: tuple с именами листов, которые нужно пропустить
        """
        self.header_row = 0  # Номер строки шапки
        self.skip_rows = tuple(skip_rows or ()) + (self.header_row, )
        self.skip_sheets = skip_sheets or ()
        self._workbook = open_workbook(file_path)

    def get_sheets(self):
        """Возвращает листы документа Excel."""
        for sheet in self._workbook.sheets():
            if sheet.name not in self.skip_sheets:
                yield sheet

    def _get_row(self):
        """Возвращает объект строки."""
        return self.row_cls()

    def _prepare_row(self, row):
        """Обрабатывает строку."""

    def _get_xls_data(self):
        """Возвращает построчно данные из документа excel."""
        for sheet in self.get_sheets():
            for row_number, data in enumerate(sheet.get_rows(), 1):
                if row_number - 1 in self.skip_rows:
                    continue

                # Пропуск пустых строк
                if not any(str(cell.value).strip() for cell in data):
                    continue

                yield sheet, row_number, data


    def get_rows(self):
        """Возвращает строки из файла."""
        for sheet, row_number, data in self._get_xls_data():
            row = self._get_row()

            row.sheet_name = sheet.name
            row.row_number = row_number

            row.values = tuple(cell.value for cell in data)

            self._prepare_row(row)

            yield row


class TestTaskParser(ExcelParser):
    """Парсер для тестового задания."""

    # названия колонок
    COLUMN_HEADERS = (
        'id', 'company', 'fact_Qlig_data1', 'fact_Qlig_data2', 'fact_Qoil_data1', 'fact_Qoil_data2',
        'forecast_Qliq_data1', 'forecast_Qliq_data2', 'forecast_Qoil_data1', 'forecast_Qoil_data2',
    )

    def _prepare_row(self, row):
        """
        Обрабатывает строку.

        Args:
            row: строка (объект ExcelRow)
        """
        row.values = dict(zip(self.COLUMN_HEADERS, row.values))
        row.values['date'] = random.choice(ALL_DATES_IN_MONTH)










