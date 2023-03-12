from pathlib import Path

from db import db as postgres_database
from loaders import TestTaskLoader
from parsers import TestTaskParser


def main():
    with postgres_database as db:
        excel_parser = TestTaskParser(
            file_path=Path(__file__).resolve().parent / 'excel' / 'test_task.xls',
            skip_rows=(1, 2),
        )
        loader = TestTaskLoader(db)
        loader.load(excel_parser.get_rows())


if __name__ == '__main__':
    main()
